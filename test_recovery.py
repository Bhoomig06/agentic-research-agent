
from app.recovery.retry import retry_operation


# Track how many times the operation runs
attempt_counter = {"count": 0}


def unreliable_operation():

    attempt_counter["count"] += 1

    # Deliberately fail on the first attempt
    if attempt_counter["count"] == 1:

        raise ConnectionError(
            "Synthetic test failure: simulated network timeout."
        )

    # Succeed on the second attempt
    return {
        "success": True,
        "message": "Operation recovered successfully."
    }


print("\nSTARTING FAILURE RECOVERY DEMONSTRATION")

result = retry_operation(
    operation=unreliable_operation,
    max_attempts=3,
    delay=1,
    operation_name="Synthetic Web Request"
)

print("\nFINAL RECOVERY RESULT")
print(result)
