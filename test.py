import magic


if magic.from_file(str(path), mime=True) == 'text/plain':
        line_px_count.append(mapcount(path))

    elif magic.from_file(str(path), mime=True) == 'image/jpeg':