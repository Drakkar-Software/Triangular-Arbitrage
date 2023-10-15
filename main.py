import asyncio
import triangular_detector.detector

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(triangular_detector.detector.run_detection())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
