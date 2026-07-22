from collections import deque
import json
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

from backend.app.context.types import GraphEdge, GraphNode, NodeType, RelationType
from backend.app.database.models import GraphEdgeModel, GraphNodeModel
from backend.app.database.repository import GraphEdgeRepository, GraphNodeRepository, UnitOfWork
from backend.app.utils.logger import logger


class ContextManager:
    """
    Enterprise Knowledge Graph Context Engine for AtherOS.
    Decoupled from NetworkX; uses native adjacency representations and persists to SQLite/PostgreSQL/Neo4j.
    The Engine, MemoryManager, Planner, and Journal communicate exclusively via ContextManager.
    """

    def __init__(self):
        # Native in-memory hot graph caches
        self._nodes: Dict[str, GraphNode] = {}
        self._outgoing: Dict[str, List[GraphEdge]] = {}
        self._incoming: Dict[str, List[GraphEdge]] = {}

    def create_node(
        self,
        node_type: NodeType | str,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        node_id: Optional[str] = None
    ) -> GraphNode:
        type_enum = NodeType(node_type) if isinstance(node_type, str) and node_type in NodeType.__members__ else node_type

        # Check existing node in memory cache
        if node_id and node_id in self._nodes:
            node = self._nodes[node_id]
            node.label = label
            if properties:
                node.properties.update(properties)
            self.update_node(node_id, properties or {})
            return node

        node = GraphNode(
            node_type=type_enum,
            label=label,
            properties=properties or {},
            node_id=node_id if node_id else str(uuid4())
        )

        self._nodes[node.node_id] = node
        if node.node_id not in self._outgoing:
            self._outgoing[node.node_id] = []
        if node.node_id not in self._incoming:
            self._incoming[node.node_id] = []

        # Database Persistence
        try:
            with UnitOfWork() as uow:
                repo = GraphNodeRepository(uow.session)
                existing = repo.get(node.node_id)
                if not existing:
                    model = GraphNodeModel(
                        id=node.node_id,
                        node_type=node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type),
                        label=node.label,
                        properties_json=json.dumps(node.properties),
                        created_at=node.created_at
                    )
                    repo.save(model)
                else:
                    existing.label = node.label
                    existing.properties_json = json.dumps(node.properties)
                    repo.update(existing)
        except Exception as err:
            logger.warning(f"Graph node database persistence warning: {err}")

        return node

    def create_edge(
        self,
        source_id: str,
        target_id: str,
        relation_type: RelationType | str,
        weight: int = 1,
        properties: Optional[Dict[str, Any]] = None
    ) -> GraphEdge:
        # Avoid duplicate edges
        rel_enum = RelationType(relation_type) if isinstance(relation_type, str) and relation_type in RelationType.__members__ else relation_type
        rel_str = rel_enum.value if hasattr(rel_enum, "value") else str(rel_enum)

        for existing in self._outgoing.get(source_id, []):
            if existing.target_id == target_id and (existing.relation_type.value if hasattr(existing.relation_type, "value") else str(existing.relation_type)) == rel_str:
                return existing

        edge = GraphEdge(
            source_id=source_id,
            target_id=target_id,
            relation_type=rel_enum,
            weight=weight,
            properties=properties or {}
        )

        if source_id not in self._outgoing:
            self._outgoing[source_id] = []
        self._outgoing[source_id].append(edge)

        if target_id not in self._incoming:
            self._incoming[target_id] = []
        self._incoming[target_id].append(edge)

        # Database Persistence
        try:
            with UnitOfWork() as uow:
                repo = GraphEdgeRepository(uow.session)
                if not repo.find_edge(source_id, target_id, rel_str):
                    model = GraphEdgeModel(
                        id=edge.edge_id,
                        source_id=source_id,
                        target_id=target_id,
                        relation_type=rel_str,
                        weight=weight,
                        properties_json=json.dumps(edge.properties),
                        created_at=edge.created_at
                    )
                    repo.save(model)
        except Exception as err:
            logger.warning(f"Graph edge database persistence warning: {err}")

        return edge

    def update_node(self, node_id: str, properties: Dict[str, Any]) -> Optional[GraphNode]:
        node = self.get_node(node_id)
        if not node:
            return None
        node.properties.update(properties)

        try:
            with UnitOfWork() as uow:
                repo = GraphNodeRepository(uow.session)
                model = repo.get(node_id)
                if model:
                    model.set_metadata(node.properties)
                    model.properties_json = json.dumps(node.properties)
                    repo.update(model)
        except Exception as err:
            logger.warning(f"Graph node update error: {err}")

        return node

    def delete_node(self, node_id: str) -> bool:
        if node_id in self._nodes:
            del self._nodes[node_id]
        if node_id in self._outgoing:
            del self._outgoing[node_id]
        if node_id in self._incoming:
            del self._incoming[node_id]

        try:
            with UnitOfWork() as uow:
                repo = GraphNodeRepository(uow.session)
                return repo.delete(node_id)
        except Exception as err:
            logger.warning(f"Graph node delete error: {err}")
            return False

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        if node_id in self._nodes:
            return self._nodes[node_id]

        try:
            with UnitOfWork() as uow:
                repo = GraphNodeRepository(uow.session)
                model = repo.get(node_id)
                if model:
                    node = GraphNode(
                        node_id=model.id,
                        node_type=NodeType(model.node_type) if model.node_type in NodeType.__members__ else model.node_type,
                        label=model.label,
                        properties=json.loads(model.properties_json or "{}"),
                        created_at=model.created_at
                    )
                    self._nodes[node_id] = node
                    return node
        except Exception as err:
            logger.warning(f"Graph get_node error: {err}")

        return None

    def query(
        self,
        node_type: Optional[NodeType | str] = None,
        properties: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[GraphNode]:
        results = []
        target_type = node_type.value if hasattr(node_type, "value") else str(node_type or "")

        for node in list(self._nodes.values()):
            curr_type = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
            if node_type and curr_type != target_type:
                continue

            if properties:
                match = True
                for k, v in properties.items():
                    if node.properties.get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            results.append(node)
            if len(results) >= limit:
                break

        return results

    def neighbors(
        self,
        node_id: str,
        direction: str = "both",
        relation_type: Optional[RelationType | str] = None
    ) -> List[GraphNode]:
        target_rel = relation_type.value if hasattr(relation_type, "value") else str(relation_type or "")
        neighbor_ids: Set[str] = set()

        if direction in ("outgoing", "both"):
            for edge in self._outgoing.get(node_id, []):
                rel_str = edge.relation_type.value if hasattr(edge.relation_type, "value") else str(edge.relation_type)
                if not relation_type or rel_str == target_rel:
                    neighbor_ids.add(edge.target_id)

        if direction in ("incoming", "both"):
            for edge in self._incoming.get(node_id, []):
                rel_str = edge.relation_type.value if hasattr(edge.relation_type, "value") else str(edge.relation_type)
                if not relation_type or rel_str == target_rel:
                    neighbor_ids.add(edge.source_id)

        return [self.get_node(nid) for nid in neighbor_ids if self.get_node(nid)]

    def traverse(
        self,
        start_node_id: str,
        max_depth: int = 3,
        strategy: str = "BFS",
        filter_relation: Optional[RelationType | str] = None,
        filter_node_type: Optional[NodeType | str] = None
    ) -> List[GraphNode]:
        """BFS or DFS graph traversal up to max_depth."""
        visited: Set[str] = set()
        result: List[GraphNode] = []

        rel_filter = filter_relation.value if hasattr(filter_relation, "value") else str(filter_relation or "")
        type_filter = filter_node_type.value if hasattr(filter_node_type, "value") else str(filter_node_type or "")

        if strategy.upper() == "BFS":
            queue = deque([(start_node_id, 0)])
            visited.add(start_node_id)

            while queue:
                curr_id, depth = queue.popleft()
                node = self.get_node(curr_id)

                if node and curr_id != start_node_id:
                    curr_type = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
                    if not filter_node_type or curr_type == type_filter:
                        result.append(node)

                if depth < max_depth:
                    for edge in self._outgoing.get(curr_id, []):
                        rel_str = edge.relation_type.value if hasattr(edge.relation_type, "value") else str(edge.relation_type)
                        if not filter_relation or rel_str == rel_filter:
                            if edge.target_id not in visited:
                                visited.add(edge.target_id)
                                queue.append((edge.target_id, depth + 1))
        else:  # DFS Strategy
            stack = [(start_node_id, 0)]
            while stack:
                curr_id, depth = stack.pop()
                if curr_id not in visited:
                    visited.add(curr_id)
                    node = self.get_node(curr_id)

                    if node and curr_id != start_node_id:
                        curr_type = node.node_type.value if hasattr(node.node_type, "value") else str(node.node_type)
                        if not filter_node_type or curr_type == type_filter:
                            result.append(node)

                    if depth < max_depth:
                        for edge in reversed(self._outgoing.get(curr_id, [])):
                            rel_str = edge.relation_type.value if hasattr(edge.relation_type, "value") else str(edge.relation_type)
                            if not filter_relation or rel_str == rel_filter:
                                stack.append((edge.target_id, depth + 1))

        return result

    def shortest_path(self, start_id: str, target_id: str) -> List[str]:
        """Finds the shortest unweighted path of node IDs from start_id to target_id using BFS."""
        if start_id == target_id:
            return [start_id]

        queue = deque([[start_id]])
        visited: Set[str] = {start_id}

        while queue:
            path = queue.popleft()
            node_id = path[-1]

            for edge in self._outgoing.get(node_id, []):
                next_id = edge.target_id
                if next_id == target_id:
                    return path + [next_id]
                if next_id not in visited:
                    visited.add(next_id)
                    queue.append(path + [next_id])

        return []

    def summarize_context(self, root_id: str) -> Dict[str, Any]:
        """Summarizes all connected context surrounding a root entity node."""
        root_node = self.get_node(root_id)
        if not root_node:
            return {"error": f"Root node '{root_id}' not found."}

        neighbors_nodes = self.neighbors(root_id, direction="both")
        outgoing_edges = self._outgoing.get(root_id, [])
        incoming_edges = self._incoming.get(root_id, [])

        return {
            "root": root_node.to_dict(),
            "outgoing_relationship_count": len(outgoing_edges),
            "incoming_relationship_count": len(incoming_edges),
            "total_connected_neighbors": len(neighbors_nodes),
            "relationships": [
                {
                    "direction": "outgoing",
                    "relation": e.relation_type.value if hasattr(e.relation_type, "value") else str(e.relation_type),
                    "target": e.target_id,
                } for e in outgoing_edges
            ] + [
                {
                    "direction": "incoming",
                    "relation": e.relation_type.value if hasattr(e.relation_type, "value") else str(e.relation_type),
                    "source": e.source_id,
                } for e in incoming_edges
            ]
        }
