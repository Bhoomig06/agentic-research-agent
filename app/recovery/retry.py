
import time


def retry_operation(
    operation,
    max_attempts=2,
    delay=1,
    operation_name="Operation"
):
    last_error = None
    attempt_errors = []

    for attempt in range(1, max_attempts + 1):

        print(
            f"\n[RECOVERY] {operation_name}: "
            f"Attempt {attempt}/{max_attempts}"
        )

        try:
            result = operation()

            if isinstance(result, dict) and not result.get("success", True):
                raise RuntimeError(
                    result.get("error", "Operation unsuccessful")
                )

            print(
                f"[RECOVERY] {operation_name} succeeded "
                f"on attempt {attempt}."
            )

            return {
                "success": True,
                "data": result,
                "attempts": attempt,
                "attempt_errors": attempt_errors,
                "error": None
            }

        except Exception as error:

            last_error = str(error)
            attempt_errors.append({
                "attempt": attempt,
                "error": last_error
            })

            print(
                f"[RECOVERY] Attempt {attempt} failed: {last_error}"
            )

            if attempt < max_attempts:
                print("[RECOVERY] Retrying operation...")
                time.sleep(delay)

    print(f"[RECOVERY] All {max_attempts} attempts failed.")

    return {
        "success": False,
        "data": None,
        "attempts": max_attempts,
        "attempt_errors": attempt_errors,
        "error": last_error
    }
