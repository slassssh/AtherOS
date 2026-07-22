import time
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, status

from backend.app.api.deps import get_engine, get_db
from backend.app.api.schemas import (
    ApiResponse,
    ChatData,
    ChatRequest,
    GoalData,
    GoalRequest,
    HealthData,
    SessionData,
    TaskData,
    VersionData,
)
from backend.app.config.config import settings
from backend.app.core.engine import Engine
from backend.app.utils.exceptions import SessionError, AtherOSError

router = APIRouter(prefix="/v1", tags=["v1"])
_START_TIME = time.time()


def _get_req_id(request: Request) -> str:
    return getattr(request.state, "request_id", "")


@router.get(
    "/health",
    response_model=ApiResponse[HealthData],
    summary="Application Health & Status",
    description="Returns application health, version, uptime, engine status, and database connection state."
)
def get_health(request: Request, engine: Engine = Depends(get_engine)):
    db = get_db()
    uptime = time.time() - _START_TIME
    health = HealthData(
        application_status="healthy",
        version=settings.version,
        uptime_seconds=round(uptime, 2),
        engine_status="operational" if engine else "degraded",
        database_status="connected" if db.connected else "disconnected"
    )
    return ApiResponse(
        data=health,
        message="System operation normal",
        request_id=_get_req_id(request)
    )


@router.get(
    "/version",
    response_model=ApiResponse[VersionData],
    summary="Application Version Details",
    description="Returns application name, semver release string, and active environment mode."
)
def get_version(request: Request):
    data = VersionData(
        app_name=settings.app_name,
        version=settings.version,
        environment=settings.environment
    )
    return ApiResponse(
        data=data,
        message="Version information retrieved",
        request_id=_get_req_id(request)
    )


@router.post(
    "/chat",
    response_model=ApiResponse[ChatData],
    summary="Interactive Chat Endpoint",
    description="Processes user input via the Engine execution pipeline and returns conversational response."
)
def post_chat(
    req: ChatRequest,
    request: Request,
    engine: Engine = Depends(get_engine)
):
    try:
        session = None
        if req.session_id:
            # Re-use existing session context via engine
            events = engine.journal.get_events_by_session(req.session_id)
            if not events:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Session '{req.session_id}' not found"
                )

        result = engine.execute_goal(req.message, session=session)
        chat_data = ChatData(
            session_id=result["session_id"],
            response=f"Goal '{req.message}' executed. Status: {result['status']}.",
            status=result["status"]
        )
        return ApiResponse(
            data=chat_data,
            message="Chat request processed",
            request_id=_get_req_id(request)
        )
    except AtherOSError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.post(
    "/goals/execute",
    response_model=ApiResponse[GoalData],
    summary="Execute High-Level Goal",
    description="Triggers the complete Engine execution pipeline (Planning -> Tool Execution -> Journaling)."
)
def execute_goal(
    req: GoalRequest,
    request: Request,
    engine: Engine = Depends(get_engine)
):
    try:
        res = engine.execute_goal(req.goal)
        goal_data = GoalData(
            session_id=res["session_id"],
            goal=res["goal"],
            status=res["status"],
            tasks=res["tasks"],
            event_count=res["event_count"]
        )
        return ApiResponse(
            data=goal_data,
            message=f"Goal execution {res['status'].lower()}",
            request_id=_get_req_id(request)
        )
    except AtherOSError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.get(
    "/sessions/{session_id}",
    response_model=ApiResponse[SessionData],
    summary="Retrieve Session Metadata",
    description="Fetches session state, titles, and event metadata by session ID."
)
def get_session_by_id(
    session_id: str,
    request: Request,
    engine: Engine = Depends(get_engine)
):
    events = engine.journal.get_events_by_session(session_id)
    if not events:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID '{session_id}' not found"
        )

    first_event = events[0]
    title = first_event.payload.get("title", "AtherOS Session")
    desc = first_event.payload.get("description", "Agent session")

    state = "COMPLETED"
    for event in reversed(events):
        if isinstance(event.payload, dict):
            if "new_state" in event.payload:
                state = event.payload["new_state"]
                break
            elif "status" in event.payload and event.payload["status"] in ("COMPLETED", "FAILED", "RUNNING"):
                state = event.payload["status"]
                break

    sess_data = SessionData(
        session_id=str(session_id),
        title=title,
        description=desc,
        state=state,
        created_at=first_event.created_at.isoformat(),
        updated_at=events[-1].created_at.isoformat()
    )
    return ApiResponse(
        data=sess_data,
        message="Session details retrieved",
        request_id=_get_req_id(request)
    )


@router.get(
    "/tasks/{task_id}",
    response_model=ApiResponse[TaskData],
    summary="Retrieve Task Details",
    description="Queries engine journal logs to locate specific task execution details by task ID."
)
def get_task_by_id(
    task_id: str,
    request: Request,
    engine: Engine = Depends(get_engine)
):
    found_payload: Any = None
    for event in engine.journal.get_events():
        if isinstance(event.payload, dict) and event.payload.get("task_id") == str(task_id):
            found_payload = event.payload

    if not found_payload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID '{task_id}' not found"
        )

    task_data = TaskData(
        task_id=str(task_id),
        description=found_payload.get("description", "Task execution"),
        tool_name=found_payload.get("tool_name") or found_payload.get("tool"),
        status=found_payload.get("status", "UNKNOWN"),
        output=found_payload.get("output"),
        error=found_payload.get("error"),
        execution_time=found_payload.get("execution_time", 0.0)
    )
    return ApiResponse(
        data=task_data,
        message="Task details retrieved",
        request_id=_get_req_id(request)
    )


@router.get(
    "/capabilities",
    summary="Discover Subsystem Capabilities",
    description="Returns registered AtherOS subsystem capabilities, health status, and metadata."
)
def get_capabilities(request: Request, engine: Engine = Depends(get_engine)):
    from backend.app.registry.capabilities import CapabilityRegistry
    registry = getattr(engine, "capability_registry", None) or CapabilityRegistry()
    return ApiResponse(
        data=registry.discover(),
        message="Capabilities retrieved successfully",
        request_id=_get_req_id(request)
    )


@router.get(
    "/events/history",
    summary="Query System Event Bus History",
    description="Returns the recent immutable event bus log history."
)
def get_event_history(request: Request, limit: int = 50, engine: Engine = Depends(get_engine)):
    from backend.app.events.bus import EventBus
    bus = getattr(engine, "event_bus", None) or EventBus()
    events = [e.to_dict() for e in bus.history(limit=limit)]
    return ApiResponse(
        data=events,
        message=f"Retrieved {len(events)} events",
        request_id=_get_req_id(request)
    )
