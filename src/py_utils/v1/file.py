import os

def tail_file(file_path, max_stats_lines):
    """Reads the last n lines from a file."""
    def read_block(file, block_size, blocks):
        """Reads a block of data from file and handles file boundaries."""
        try:
            file.seek(blocks * block_size, os.SEEK_END)
        except IOError:  # handle file too small for block size
            file.seek(0)
            return file.read()
        else:
            return file.read(block_size)

    with open(file_path, 'rb') as file:
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        block_size = 1024
        blocks = -1
        data = b''

        while abs(blocks) * block_size < file_size:
            data = read_block(file, block_size, blocks) + data
            if data.count(b'\n') >= max_stats_lines + 1:
                break
            blocks -= 1

        # Process and yield each line in natural order
        lines = data.splitlines()[-max_stats_lines:]
        for line in reversed(lines):  # Reverse the list to maintain natural order
            yield line.decode('utf-8')

