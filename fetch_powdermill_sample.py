"""Retrieve one CC0 MP3 or WAV from a remote ZIP via validated byte ranges."""
import argparse
import io
import hashlib
import urllib.request
import zipfile
from pathlib import Path

SOURCES = {
    "mp3": ("mp3_Files.zip", 182276751, 8_000_000,
            "3cc6aadb45c7adbf44f2f514686a16bc2965a9d87446763cf95dff3fce22c789"),
    "wav": ("wav_Files.zip", 1428295296, 30_000_000,
            "1bca5e38addcc3d5b37e76f06feaae53051b1ff231e8234bc59628a6d81ce046"),
}


class RangeFile(io.RawIOBase):
    def __init__(self, url, size, limit):
        self.url, self.size, self.limit = url, size, limit
        self.pos = 0
        self.transferred = 0

    def readable(self):
        return True

    def seekable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, offset, whence=io.SEEK_SET):
        position = offset if whence == io.SEEK_SET else self.pos + offset if whence == io.SEEK_CUR else self.size + offset
        if not 0 <= position <= self.size:
            raise ValueError("Seek outside archive")
        self.pos = position
        return position

    def read(self, n=-1):
        if n < 0:
            n = self.size - self.pos
        n = min(n, self.size - self.pos)
        if not n:
            return b""
        if self.transferred + n > self.limit:
            raise ValueError("Download limit exceeded")
        end = self.pos + n - 1
        request = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}",
                                                      "User-Agent": "CorvidObservatory/1.0 (scientific research)"})
        with urllib.request.urlopen(request, timeout=60) as response:
            expected = f"bytes {self.pos}-{end}/{self.size}"
            if response.status != 206 or response.headers.get("Content-Range") != expected:
                raise ValueError("Server did not return the requested byte range")
            data = response.read(n + 1)
        if len(data) != n:
            raise ValueError("Truncated or unexpected range response")
        self.pos += n
        self.transferred += n
        return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=SOURCES, default="mp3")
    args = parser.parse_args()
    archive_name, size, limit, expected_hash = SOURCES[args.format]
    url = f"https://zenodo.org/api/records/4656848/files/{archive_name}/content"
    member_ext = "WAV" if args.format == "wav" else "mp3"
    member = f"Recording_1/Recording_1_Segment_22.{member_ext}"
    output = Path(f"data/powdermill/Recording_1_Segment_22.{args.format}")
    remote = RangeFile(url, size, limit)
    with zipfile.ZipFile(remote) as archive:
        info = archive.getinfo(member)
        if info.file_size > limit or info.compress_size > limit:
            raise ValueError("Member exceeds download limit")
        audio = archive.read(info)  # zipfile verifies the member's CRC-32.
    if expected_hash and hashlib.sha256(audio).hexdigest() != expected_hash:
        raise ValueError("Sample SHA-256 differs from the recorded source")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(audio)
    print(f"Wrote {output} ({len(audio)} bytes); transferred {remote.transferred} bytes; SHA-256 {hashlib.sha256(audio).hexdigest()}")


if __name__ == "__main__":
    main()
