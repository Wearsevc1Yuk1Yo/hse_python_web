from task2Processes.monitorResults import monitor
import asyncio

import signal

running = True

def signal_handler(sig, frame):
    global running
    print("\n Work done...")
    running = False

async def main():
    global running
    signal.signal(signal.SIGINT, signal_handler)
    # чтобы стопить безумие

    try:

        # задача мониторинга
        monitor_task = asyncio.create_task(monitor())
        while running:
            await asyncio.sleep(0.1)
        monitor_task.cancel()
        # обработчик сигнала
        try:
            await monitor_task
        except asyncio.CancelledError:
            print("Monitoring stopped")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
