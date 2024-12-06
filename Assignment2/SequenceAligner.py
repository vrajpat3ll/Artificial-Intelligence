from dataclasses import dataclass
from typing import List
import heapq
from enum import Enum

# Constants for alignment costs
MATCH_COST = 0
MISMATCH_COST = 2
GAP_COST = 3


class Operation(Enum):
    MATCH = "match"
    MISMATCH = "mismatch"
    GAP_IN_SEQ1 = "gap_in_seq1"
    GAP_IN_SEQ2 = "gap_in_seq2"


@dataclass
class AlignmentState:
    """Represents a state in the alignment process"""
    i: int                          # Position in sequence 1
    j: int                          # Position in sequence 2
    cost: float                     # Current cost
    operations: List[Operation]     # List of operations performed
    alignment1: str                 # Current alignment for sequence 1
    alignment2: str                 # Current alignment for sequence 2

    def __lt__(self, other):
        # comparing f-value, as this problem satisfies monotone condition
        return self.cost + self.heuristic() < other.cost + other.heuristic()

    def heuristic(self) -> float:
        """
        Heuristic function estimating minimum cost to complete alignment
        Uses the difference in remaining lengths and minimum possible operation costs
        """
        remaining_seq1 = len(self.alignment1) - self.i
        remaining_seq2 = len(self.alignment2) - self.j
        length_diff = abs(remaining_seq1 - remaining_seq2)

        # Minimum number of gaps needed is the difference in remaining lengths
        min_gaps = length_diff

        # Minimum number of operations needed for the shorter remaining sequence
        min_remaining = min(remaining_seq1, remaining_seq2)

        # Best case: all matches for min_remaining and gaps for length difference
        return min_gaps * GAP_COST


class SequenceAligner:
    def __init__(self, sequence1: str, sequence2: str):
        self.seq1 = sequence1.upper()
        self.seq2 = sequence2.upper()

    def get_next_states(self, state: AlignmentState) -> List[AlignmentState]:
        """Generate all possible next states from current state"""
        next_states = []

        # Check if we've reached the end of either sequence
        if state.i >= len(self.seq1) and state.j >= len(self.seq2):
            return next_states

        # Case 1: Gap in sequence 1
        if state.j < len(self.seq2):
            new_alignment1 = state.alignment1 + "-"
            new_alignment2 = state.alignment2 + self.seq2[state.j]
            new_operations = state.operations + [Operation.GAP_IN_SEQ1]
            next_states.append(AlignmentState(
                state.i,
                state.j + 1,
                state.cost + GAP_COST,
                new_operations,
                new_alignment1,
                new_alignment2
            ))

        # Case 2: Gap in sequence 2
        if state.i < len(self.seq1):
            new_alignment1 = state.alignment1 + self.seq1[state.i]
            new_alignment2 = state.alignment2 + "-"
            new_operations = state.operations + [Operation.GAP_IN_SEQ2]
            next_states.append(AlignmentState(
                state.i + 1,
                state.j,
                state.cost + GAP_COST,
                new_operations,
                new_alignment1,
                new_alignment2
            ))

        # Case 3: Match or Mismatch
        if state.i < len(self.seq1) and state.j < len(self.seq2):
            is_match = self.seq1[state.i] == self.seq2[state.j]
            new_cost = state.cost + (MATCH_COST if is_match else MISMATCH_COST)
            new_operations = state.operations + \
                [Operation.MATCH if is_match else Operation.MISMATCH]
            new_alignment1 = state.alignment1 + self.seq1[state.i]
            new_alignment2 = state.alignment2 + self.seq2[state.j]
            next_states.append(AlignmentState(
                state.i + 1,
                state.j + 1,
                new_cost,
                new_operations,
                new_alignment1,
                new_alignment2
            ))

        return next_states

    def align(self):
        """
        Perform sequence alignment using A* search
        Returns: (aligned_seq1, aligned_seq2, total_cost, operations)
        """
        # Initialize start state
        start_state = AlignmentState(0, 0, 0, [], "", "")

        # Priority queue for A* search
        open_list = [start_state]
        heapq.heapify(open_list)

        # Set to track visited states
        closed_set = set()

        while open_list:
            current_state = heapq.heappop(open_list)

            # Check if we've reached the goal (both sequences fully aligned)
            if current_state.i == len(self.seq1) and current_state.j == len(self.seq2):
                return (
                    current_state.alignment1,
                    current_state.alignment2,
                    current_state.cost,
                    current_state.operations
                )

            # Generate state signature for visited set
            state_signature = (current_state.i, current_state.j)
            if state_signature in closed_set:
                continue

            closed_set.add(state_signature)

            # Generate and add next possible states
            for next_state in self.get_next_states(current_state):
                heapq.heappush(open_list, next_state)

        # No alignment found (shouldn't happen with valid sequences)
        return None

    def visualize_alignment(self, aligned_seq1: str, aligned_seq2: str, operations: List[Operation]) -> str:
        """Create a visual representation of the alignment"""
        result = []
        result.append("Sequence Alignment:")
        result.append(f"Sequence 1: {aligned_seq1}")
        result.append(f"            {''.join(
            '|' if op == Operation.MATCH else ' ' for op in operations)}")
        result.append(f"Sequence 2: {aligned_seq2}")
        return '\n'.join(result)


def main():
    # Example sequences
    seq1 = "AGCTGATC"
    seq2 = "GCTAGC"

    print(f"Sequence 1: {seq1}")
    print(f"Sequence 2: {seq2}")
    print("\nPerforming sequence alignment...\n")

    # Create aligner and perform alignment
    aligner = SequenceAligner(seq1, seq2)
    result = aligner.align()

    if result:
        aligned_seq1, aligned_seq2, cost, operations = result

        # Print results
        print(aligner.visualize_alignment(
            aligned_seq1, aligned_seq2, operations))
        print(f"\nAlignment Cost: {cost}")

        # Print operation details
        print("\nAlignment Operations:")
        for i, op in enumerate(operations, 1):
            print(f"Step {i}:".ljust(8)+f" {op.value}")

        # Print statistics
        print("\nAlignment Statistics:")
        op_counts = {}
        for op in Operation:
            op_counts[op] = operations.count(op)
        for op, count in op_counts.items():
            print(f"{op.value}: {count}")

    else:
        print("No alignment found!")


if __name__ == "__main__":
    main()
