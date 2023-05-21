import subprocess


def name_to_tag(name: str) -> str:
    return name.lower().replace(" ", "_")


def chunks(lst: list, n: int) -> list[list]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def run_concurrent_stress_test(stress_test_nr: int, num_clients: int = 2):
    if stress_test_nr < 2 or stress_test_nr > 4:
        raise ValueError("Stress test number must be between 2 and 4")
    module_name = f"rental.concurrent.stress_test_{stress_test_nr}"
    processes = []
    for _ in range(num_clients):
        processes.append(
            subprocess.Popen(
                ["python", "-m", module_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        )
    [p.wait() for p in processes]
    for i, p in enumerate(processes):
        print(f"Process {i}")
        print("Output:")
        print(p.stdout.read())
        print("Errors:")
        print(p.stderr.read())
        print("==========")
