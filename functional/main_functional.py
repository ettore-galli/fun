from functional.functional_base import ExecutionContext, Issue, IssueType
from functional.mail_message_core import (
    MailMessage,
    RunEnvironment,
    log_issues,
    # send_message_utility,
    validate_message_utility,
)

EmailContext = ExecutionContext[MailMessage, RunEnvironment]


def validation_step(context: EmailContext) -> EmailContext:
    errors = validate_message_utility(context.payload)
    return context.with_issues(
        new_issues=[
            Issue(issue_type=IssueType.ERROR, message=message) for message in errors
        ]
    )


def log_step(context: EmailContext) -> EmailContext:
    log_errors = log_issues(
        run_environment=context.environment,
        log_messages=[
            f"{issue.issue_type.value}: {issue.message}" for issue in context.issues
        ],
    )

    return context.with_issues(
        new_issues=[
            Issue(issue_type=IssueType.ERROR, message=message) for message in log_errors
        ]
    )


# pylint: disable=duplicate-code
def send_mail_functional(
    sender: str, recipient: str, subject: str, text: str
) -> EmailContext:
    mail_message = MailMessage(
        sender=sender,
        recipient=recipient,
        subject=subject,
        text=text,
    )

    run_environment: RunEnvironment = RunEnvironment(
        smtp_server="my-server", log_file="./log.txt"
    )

    context: EmailContext = EmailContext(
        environment=run_environment,
        payload=mail_message,
    )

    validation = validation_step(context=context)

    logged = log_step(validation)

    final = logged
    # validation_errors = validate_message_utility(mail_message=mail_message)

    # if len(validation_errors) > 0:
    #     log_errors = log_issues(
    #         run_environment=run_environment, log_messages=validation_errors
    #     )
    #     if len(log_errors) > 0:
    #         return validation_errors + log_errors
    #     return validation_errors

    # send_errors = send_message_utility(
    #     run_environment=run_environment, mail_message=mail_message
    # )

    # if len(send_errors) > 0:
    #     log_errors = log_issues(
    #         run_environment=run_environment, log_messages=validation_errors
    #     )
    #     if len(log_errors) > 0:
    #         return send_errors + log_errors
    #     return send_errors

    return final


# pylint: disable=duplicate-code
if __name__ == "__main__":
    print("===== CASE1: (Errors)")
    print(
        send_mail_functional(
            sender="myself",
            recipient="destination@some.address",
            subject="A Subject",
            text="A Message...",
        )
    )

    print("===== CASE2: (Ok)")
    print(
        send_mail_functional(
            sender="myself@my.address",
            recipient="destination@some.address",
            subject="A Subject",
            text="A Message...",
        )
    )
