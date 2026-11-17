from typing import List
import httpx

"""
Асинхронно получает матрицу по URL и возвращает список элементов,
обходя её против часовой стрелки, начиная с левого верхнего угла.
"""
async def get_matrix(url: str) -> List[int]:
    # Загрузка данных с обработкой сетевых ошибок и статусов
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        raise RuntimeError(f"Ошибка при получении данных с сервера: {e}")

    # Парсинг матрицы
    matrix = []
    for line in response.text.strip().splitlines():
        if '|' in line:
            row = [int(p.strip()) for p in line.split('|') if p.strip()]
            if row:
                matrix.append(row)

    if not matrix:
        return []

    # Алгоритм обхода по спирали против часовой стрелки
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Вниз по левому столбцу
        for r in range(top, bottom + 1):
            result.append(matrix[r][left])
        left += 1
        if left > right:
            break

        # Вправо по нижней строке
        for c in range(left, right + 1):
            result.append(matrix[bottom][c])
        bottom -= 1
        if top > bottom:
            break

        # Вверх по правому столбцу
        for r in range(bottom, top - 1, -1):
            result.append(matrix[r][right])
        right -= 1
        if left > right:
            break

        # Влево по верхней строке
        for c in range(right, left - 1, -1):
            result.append(matrix[top][c])
        top += 1

    return result

