from collections import Counter


def read_file(filename):
    """Read the input file."""
    with open(filename, "r", encoding="utf-8") as f:
        n = f.readline()
        n.strip("\n")
    return n


def check_marker_chunk(string: str):
    """
    Check if a chunk of the string is a marker.

    A string is a marker if it contains unique items, ie letters are
    not repeated. If length of input and counts of each letter matches,
    it can be considered a marker.

    Parameters
    ----------
    string : str
        Input chunk of string.

    Returns
    -------
    bool
        If the chunk of string is a marker or not.
    """
    n = len(string)
    counts = Counter()
    counts.update(string)
    return n == len(counts)


def check_chunks(string: str, chunk_size=4):
    """Given a message string, check chunks of size chunk_size
    iteratively for a marker.

    Parameters
    ----------
    string : str
        Full message string of len>chunk_size
    chunk_size : int, optional
        Length of the chunk (sub-string) to check for marker, by default 4

    Returns
    -------
    Tuple: str, int
        Chunk of chunk_size identified as marker and its (end) position.
    """
    for start in range(len(string) - chunk_size + 1):
        end = start + chunk_size
        chunk = string[start:end]
        print(start, end, chunk)
        if check_marker_chunk(chunk):
            return chunk, end


if __name__ == "__main__":
    message = read_file("dec6/input.txt")
    print(message)
    # message = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    marker, pos = check_chunks(message, 14)
    print(f"got marker: {marker} at {pos}")
