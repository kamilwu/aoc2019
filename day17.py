from typing import Generator
from typing import List
from typing import Tuple

import day9


class CameraOutput(day9.OutDevice):
    def __init__(self):
        self._output: List[int] = []
        self._intersections: List[int] = []
        self.width: int = -1

    def out(self, item: int) -> None:
        if item == ord('\n'):
            if self.width == -1:
                self.width = len(self._output)
        else:
            self._output.append(item)

    def print(self) -> None:
        for i, ch in enumerate(self._output):
            if i % self.width == 0:
                print()
            print(chr(ch), end='')
        print()

    def _get_neighbours(self, index: int) -> Tuple[int, int, int, int]:
        return index - 1, index - self.width, index + 1, index + self.width

    def _put_intersections(self) -> None:
        for i in self._intersections:
            self._output[i] = ord('O')

    def _calculate_intersections(self) -> None:
        for i, ch in enumerate(self._output):
            if ch != ord('#'):
                continue

            neighbours = self._get_neighbours(i)
            is_intersection = True
            for neighbour in neighbours:
                try:
                    n_ch = self._output[neighbour]
                    if n_ch != ord('#'):
                        is_intersection = False
                        break
                except IndexError:
                    # at the boundary, definitely not an intersection
                    is_intersection = False
                    break

            if is_intersection:
                self._intersections.append(i)

        self._put_intersections()

    def get_alignment_parameters(self) -> Generator[int, None, None]:
        self._calculate_intersections()
        for intersection in self._intersections:
            yield (intersection // self.width) * (intersection % self.width)


if __name__ == '__main__':
    program = day9.get_puzzle('data/day17.txt')
    camera_output = CameraOutput()
    day9.program_loop(program, None, camera_output)

    alignment_parameters_sum = sum(camera_output.get_alignment_parameters())
    camera_output.print()
    print(alignment_parameters_sum)
