import urllib.request, urllib.error, certifi, ssl, datetime as dt, sqlite3

from docopt import docopt

def recorder(url, filename, duration, blocksize):
    """Record audio stream from the given URL."""
    if int(duration) < 1:
        raise ValueError("Duration cannot be smaller than 1!")
    if int(blocksize) < 1:
        raise ValueError("Blocksize cannot be smaller than 1!")
    if filename is None:
        now = dt.datetime.now()
        filename = now.strftime("%Y-%m-%d-%H-%M-%S")

    print(f"Recording from {url} to {filename}.mp3 for {duration} seconds with blocksize {blocksize}")
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    try:
        stream = urllib.request.urlopen(url, context=ssl_context)
        stream_bitrate = 128 * int(stream.headers.get('icy-br'))
        start_time = dt.datetime.now()
        blocks_target = int(duration) * stream_bitrate / int(blocksize)
        blocks_written = 0

        with open(f"{filename}.mp3", 'wb') as f:
            while blocks_written < blocks_target:
                f.write(stream.read(int(blocksize)))
                blocks_written += 1



        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS recordings
                     (identifier INTEGER PRIMARY KEY, url TEXT, filename TEXT, date TEXT, time TEXT, duration INTEGER)''')
        c.execute("INSERT INTO recordings (url, filename, date, time, duration) VALUES (?, ?, ?, ?, ?)",
                  (url, filename, start_time.date().isoformat(), start_time.time().strftime("%H:%M:%S"), duration))
        conn.commit()
        print("\nRecording successfully saved and logged in database.\n")
        list_recordings(0)
        conn.close()
    except urllib.error.HTTPError:
        print("\nERROR: A HTTP error occurred while attempting to connect to the resource. Please check the URL.")
    except TypeError:
        print("\nERROR: The provided URL does not have a valid mp3 stream")
    except ValueError:
        print("\nERROR: The provided URL is not a valid web resource.")

def list_recordings(fetch_all):
    """List all recordings from the database."""
    try:
        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM recordings")
        count = c.fetchone()[0]
        if count == 0:
            print("The database currently contains no recordings!")
        else:
            if fetch_all:
                c.execute("SELECT * FROM recordings")
                rows = c.fetchall()
            else:
                c.execute("SELECT * FROM recordings ORDER BY identifier DESC LIMIT 1")
                rows = c.fetchall()
            print(f"{'IDs':3}{'Title':>20}   {'URL':<60}{'Date':>15}{'Timestamp':>15}{'Length':>10}")
            for row in rows:
                identifier, url, title, date, time, duration = row
                print(f"{identifier:3}{title:>20}   {url:<60}{date:>15}{time:>15}{duration:>10}")
        conn.close()
    except sqlite3.OperationalError:
        print("\nERROR: An error occurred while reading the database. It may not exist or be corrupted.")

def clear_database():
    """Clears all entries from the database"""
    try:
        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()
        # noinspection SqlWithoutWhere
        c.execute("DELETE FROM recordings")
        conn.commit()
        conn.close()
        return "The database has been cleared"
    except sqlite3.OperationalError:
        return "\nERROR: The database does not exist yet"

def main():
    """Main entry point for the script."""
    doc = """Audiorecorder

    Usage:
      cli_audiorecorder.py <url> [--filename=<name> --duration=<time> --blocksize=<size>]
      cli_audiorecorder.py -l | --list
      cli_audiorecorder.py -h | --help
      cli_audiorecorder.py -c | --clear

    Options:
      -h --help             Show this screen.
      --filename=<name>     Name of recording.
      --duration=<time>     Duration of recording in seconds [default: 5].
      --blocksize=<size>    Block size for read/write in bytes [default: 128].
      -l --list             List all recordings.
      -c --clear            Clear the database.
    """
    arguments = docopt(doc)

    if arguments['--list']:
        list_recordings(1)
    elif arguments['--clear']:
        print(clear_database())
    else:
        url = arguments['<url>']
        filename = arguments['--filename']
        duration = arguments['--duration']
        blocksize = arguments['--blocksize']
        recorder(url, filename, duration, blocksize)

if __name__ == '__main__':
    main()
