class Device:
    def __init__(self, name: str, connected_by: str) -> None:
        self.name = name
        self.connected_by = connected_by
        self.connected = True

    def __str__(self) -> str:
        # !r - Print with quotes
        return f"Device {self.name!r} ({self.connected_by!r})"

    def disconnect(self):
        self.connected = False
        print("Disconnected")


class Printer(Device):
    def __init__(self, name: str, connected_by: str, capacity: int) -> None:
        super().__init__(name, connected_by)
        self.capacity = capacity
        self.remaining_pages = capacity

    def __str__(self) -> str:
        return f"{super().__str__()} ({self.remaining_pages} pages remaining)"

    def print(self, pages: int):
        if not self.connected:
            print("Your printer is not connected!")
            return

        print("Printing {pages} pages.")
        self.remaining_pages -= pages


printer = Printer("Printer", "USB", 500)
printer.print(20)

print(printer)

printer.disconnect()
printer.print(30)
