import logging
import os

logger = logging.getLogger(__name__)
MAX_RETRIES = 3


async def validate_node(state: dict) -> dict:
    pending = state.get("pending_stories", [])
    validated = state.get("validated_stories", [])
    retry_counts = state.get("retry_counts", {})

    if not pending:
        return state

    failed = []
    for story in pending:
        story_id = story.get("id") or story.get("title", "unknown")
        retry_counts[story_id] = retry_counts.get(story_id, 0) + 1

        summary = story.get("summary")
        image_prompt = story.get("image_prompt")
        image_path = story.get("image_path")          # <-- new check
        errors = []

        # Validate summary
        if not summary:
            errors.append("Missing summary object")
        else:
            if not summary.get("summary"):
                errors.append("Missing summary text")
            if not summary.get("why_it_matters"):
                errors.append("Missing 'why it matters'")
            if not summary.get("key_points") or len(summary.get("key_points", [])) < 2:
                errors.append("Need at least 2 key points")

        # Validate image prompt
        if not image_prompt or len(image_prompt) < 10:
            errors.append("Image prompt missing or too short")

        # ---- NEW: Validate image exists ----
        if not image_path:
            errors.append("Image generation failed – no image path")
        elif not os.path.exists(image_path):
            errors.append(f"Image file missing: {image_path}")
        # -----------------------------------

        if errors:
            story["validation_errors"] = errors
            if retry_counts[story_id] < MAX_RETRIES:
                logger.warning(f"Validation failed for '{story.get('title', '')[:40]}...' (retry {retry_counts[story_id]}/{MAX_RETRIES})")
                # Clear the generated data so they are regenerated on retry
                story.pop("summary", None)
                story.pop("image_prompt", None)
                story.pop("image_path", None)
                failed.append(story)
            else:
                logger.error(f"Story '{story.get('title', '')[:40]}...' failed after {MAX_RETRIES} retries. Discarding.")
        else:
            story["validation_errors"] = []
            validated.append(story)
            logger.info(f"Validation passed for '{story.get('title', '')[:40]}...'")

    state["pending_stories"] = failed
    state["validated_stories"] = validated
    state["retry_counts"] = retry_counts
    state["should_retry"] = bool(failed)

    return state