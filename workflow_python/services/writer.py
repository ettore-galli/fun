import time


def write_output(entry_data: str, output_file_name) -> None:
    with open(output_file_name, "w") as output_file:
        line = "*" * 80 + "\n"
        time.sleep(0.07)
        output_file.write(line)
        output_file.write(entry_data)
        output_file.write(line)

