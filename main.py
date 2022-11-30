from functools import reduce

from PIL import Image, ImageDraw


def transform(point):
    return point[1], -point[0] + (540 + 1)


def angle(p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]) -> int:
    return (p2[0] - p1[0]) * (p3[1] - p2[1]) - (p2[1] - p1[1]) * (p3[0] - p2[0])


def ConvexHull(pointList: list[tuple[int, int]]) -> list[tuple[int, int]]:
    firstPoint = reduce(lambda p1, p2: p2 if p2[0] < p1[0] or (p2[0] == p1[0] and p2[1] < p1[1]) else p1, pointList)

    convexHull = [firstPoint]
    pointList.remove(firstPoint)
    pointList.append(firstPoint)

    while True:
        currentPoint = convexHull[-1]
        p1 = pointList[0]
        for p2 in pointList[1:]:
            if angle(currentPoint, p1, p2) < 0:
                p1 = p2

        if p1 != firstPoint:
            convexHull.append(p1)
            pointList.remove(p1)
        else:
            break

    return convexHull


def main():
    with open("DS8.txt", "r") as file:
        lines = file.readlines()

    pointList = []
    for line in lines:
        coords = line.strip().split(" ")
        x = int(coords[0])
        y = int(coords[1])
        point = (x, y)
        pointList.append(transform(point))

    convexHull = ConvexHull(pointList[::])
    with open('ConvexHull.txt', 'w') as file:
        for point in convexHull:
            file.write(f'{point[0]} {point[1]}\n')

    image = Image.new("RGB", (960, 540))
    draw = ImageDraw.Draw(image)

    for point in pointList:
        draw.point(point, fill="white")

    for i in range(len(convexHull) - 1):
        draw.line(convexHull[i] + convexHull[i + 1], fill='blue')
    draw.line(convexHull[-1] + convexHull[0], fill='blue')

    image.save('result.png')


if __name__ == "__main__":
    main()
