from typing import List
from functional.etl_workflows.single.mail_message_core import (
    MailMessage,
    RunEnvironment,
    log_issues,
    send_message_utility,
    validate_message_utility,
)


# pylint: disable=duplicate-code
def send_mail_nonfunctional(
    sender: str, recipient: str, subject: str, text: str
) -> List[str]:
    mail_message = MailMessage(
        sender=sender,
        recipient=recipient,
        subject=subject,
        text=text,
    )

    run_environment: RunEnvironment = RunEnvironment(
        smtp_server="my-server", log_file="/tmp/log.txt"
    )

    validation_errors = validate_message_utility(mail_message=mail_message)

    if len(validation_errors) > 0:
        log_errors = log_issues(
            run_environment=run_environment, log_messages=validation_errors
        )
        if len(log_errors) > 0:
            return validation_errors + log_errors
        return validation_errors

    send_errors = send_message_utility(
        run_environment=run_environment, mail_message=mail_message
    )

    if len(send_errors) > 0:
        log_errors = log_issues(
            run_environment=run_environment, log_messages=validation_errors
        )
        if len(log_errors) > 0:
            return send_errors + log_errors
        return send_errors

    return []


# pylint: disable=duplicate-code
if __name__ == "__main__":
    print("===== CASE1: (Errors)")
    result_1 = send_mail_nonfunctional(
        sender="myself",
        recipient="destination@some.address",
        subject="A Subject",
        text="A Message...",
    )
    print(result_1)

    print("===== CASE2: (Ok)")
    result_2 = send_mail_nonfunctional(
        sender="myself@my.address",
        recipient="destination@some.address",
        subject="A Subject",
        text="A Message...",
    )
    print(result_2)
