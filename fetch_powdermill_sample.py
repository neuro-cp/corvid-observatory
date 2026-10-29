"""Retrieve one public-domain MP3 from a remote ZIP via validated byte ranges."""
import io
import hashlib
import urllib.request
import zipfile
from pathlib import Path

URL = "https://zenodo.org/api/records/4656848/files/mp3_Files.zip/content"
SIZE = 182276751  # Published record size; range responses are checked against it.
MEMBER = "Recording_1/Recording_1_Segment_22.mp3"
OUTPUT = Path("data/powdermill/Recording_1_Segment_22.mp3")
MAX_DOWNLOAD = 8_000_000
EXPECTED_SHA256 = "3cc6aadb45c7adbf44f2f514686a16bc2965a9d87446763cf95dff3fce22c789"


class RangeFile(io.RawIOBase):
    def __init__(self):
        self.pos = 0
        self.transferred = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        position = offset if whence == io.SEEK_SET else self.pos + offset if whence == io.SEEK_CUR else SIZE + offset
        if not 0 <= position <= SIZE:
            raise ValueError("Seek outside archive")
        self.pos = position
        return position

    def read(self, n=-1):
        if n < 0:
            n = SIZE - self.pos
        n = min(n, SIZE - self.pos)
        if not n:
            return b""
        if self.transferred + n > MAX_DOWNLOAD:
            raise ValueError("Download limit exceeded")
        end = self.pos + n - 1
        request = urllib.request.Request(URL, headers={"Range": f"bytes={self.pos}-{end}",
                                                      "User-Agent": "CorvidObservatory/1.0 (scientific research)"})
        with urllib.request.urlopen(request, timeout=60) as response:
            expected = f"bytes {self.pos}-{end}/{SIZE}"
            if response.status != 206 or response.headers.get("Content-Range") != expected:
                raise ValueError("Server did not return the requested byte range")
            data = response.read(n + 1)
        if len(data) != n:
            raise ValueError("Truncated or unexpected range response")
        self.pos += n
        self.transferred += n
        return data


def main():
    remote = RangeFile()
    with zipfile.ZipFile(remote) as archive:
        info = archive.getinfo(MEMBER)
        if info.file_size > MAX_DOWNLOAD or info.compress_size > MAX_DOWNLOAD:
            raise ValueError("Member exceeds download limit")
        audio = archive.read(info)  # zipfile verifies the member's CRC-32.
    if hashlib.sha256(audio).hexdigest() != EXPECTED_SHA256:
        raise ValueError("Sample SHA-256 differs from the recorded source")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(audio)
    print(f"Wrote {OUTPUT} ({len(audio)} bytes); transferred {remote.transferred} bytes")


if __name__ == "__main__":
    main()
