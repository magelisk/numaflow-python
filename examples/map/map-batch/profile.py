import json
import base64
import numpy as np
from line_profiler import line_profiler
profile = line_profiler.LineProfiler()

SINGLE_RAW = {"Data": {"padding": '7QXXgu2/66d9nOnw5TigPXFJlOAzC2Mp82IO/MG7Bxv0jpUWz3w72qQyJIh+EGu6i8pW5F581dkjV4vMK+vJ0PnFj8QCfNTWi+CfamAAOUR1vKmHTvVHoNe5ZwyAzCMTiSuDSlfbHEyCvBoQaO7bOmOCNIxpxzLOsfyaEqrmJ1JUHrAswX2BomKKq8Qm645bdTNp2L/lHgSG5XyR0MuK1OfMmHogLlzpRXJnRdhEpWfj5xyDpRUW4C+WlJDHmQ7SrzFegoR+Jp5HpTI0GuQz9czvmyW8qYpGWtYdyWyFEvpNPoFb6b5P6Ce/ee2xGoHjXtQIOg/cjf5Eo3evQ/2ggZdv9ShWlMdaZxHP7zTiq0sdTYE8i95k3DHz6ecMJbzYh4XSlohGnePHhxde3Ur0G9L7NOY6nuFBSSOAGReMmq58if9/Eu93QknOavXP0eHnIXTglU/lTIw/rqYC6DHo8sMecYO4tve8TJhRHamJHzejayQQNQIABiASmuNmvyNqSBPunhBuBWrCGxAqcahzWSazJ3xP+zCEqhW9Wq+gk02XXuZnf+8Xc035tS58MtgfxAeVhoDskSq18SpbRzk0C+OBB7JbD7sXG1+JosgBMnL74j38hzoJV8y3+X0mDSN/qAXkYDjVJ13+ihkU4SPIsdXzxVQw+fjDNON3aAIlyhgJs9bXRfTX2r019EFWQdHovU/THC/uARL64ij14fFsHPxXjadqP9eNR/Bvk7R2n29zavOxfaisU6YlW8+zUz/DcE0+E7hbktDrb4w4GcYxp2gZNHv3j2TVrDmoWTdFACDifu443XZGqmcpHatgZupVCTUksW6CeWA1NrgJrAI0d0ouc0UW+6zweHGxSekNr30pxbRmBTNPmsjPQpRsG1pmvLnJ2G6aGQLUfYbzeVxLS/ogdspqt6bpQjWmoof56EDeGpFGEn9zVc/xTUe5uOO0pmg1hL4xsgTEb+POjjw6KmzSks1Mtl045OQ+PnwqOMc30vycYzIMSzO3pOYmrkl/pPKgdqYOHNPYyqSCVTJIoDOZsAaS+SWHdoubhophwtybIJluM4aj0VjcUwi4eoRiuHkq0hfPgeQHuF8U3PD+YLQAeznjSAETzAnj1Gzrrvi61TkNZFVt85NU8O89tJshjKtTnWWC9U52gdXFa8Wt/rVrl9uqSPJ+Ov7rvzXW4XJP3v01xeXq1++kBzIDwA9tram/94nLI3qFvl1Tv45119A4mnVkL1+LUDYiNKl5tZLuTzgSL0zVF7a4M68trJaN5q/Nuhsws4DMv5Oy4ewBItG/EX0wZ6u0LnrD9erElKfufBMFUZy23xgV2Y=='}}
SINGLE = json.dumps(SINGLE_RAW).encode("utf-8")
GROUP = [SINGLE] * 1000


def b64_to_array(b64_data):
    data_bytes = base64.b64decode(b64_data)
    return np.frombuffer(data_bytes, dtype=np.uint8) * 1.0j

@profile
def mulitple():
    batch = []
    for msg in GROUP:
        parsed = json.loads(msg.decode())
        data_bytes = base64.b64decode(parsed["Data"]["padding"])
    
        batch.append(data_bytes)

    as2d = np.frombuffer(np.array(batch), dtype=np.uint8) * 1.0j
    # as2d = np.array(batch)
    # x1 = as2d*2
    np.multiply(as2d, as2d, out=as2d)
    # result = np.fft.fft(as2d)
    print("Return group")
    # yield Message(value=result.tobytes(), tags=["grouped"])
    
    serialized = as2d.tobytes()
    return serialized


@profile
def single():
    for msg in GROUP:
        parsed = json.loads(msg.decode())
        # arr = b64_to_array(parsed["Data"]["padding"])
        data_bytes = base64.b64decode(parsed["Data"]["padding"])
        arr = np.frombuffer(np.array(data_bytes), dtype=np.uint8) * 1.0j

        # x1 = arr*2
        np.multiply(arr, arr, out=arr)
        # result = np.fft.fft(arr)
        serialized = arr.tobytes()


single()
res = mulitple()
print(len(res))

profile.print_stats()