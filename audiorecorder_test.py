import cli_audiorecorder, unittest, sqlite3, os

class AudiorecorderTest(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        self.url = "https://www.antennebrandenburg.de/livemp3"
        self.filename = "test_recording"
        self.duration = 5
        self.blocksize = 128
        cli_audiorecorder.clear_database()

    def tearDown(self):
        """Delete the temporarily created test recording"""
        if os.path.exists(f"{self.filename}.mp3"):
            os.remove(f"{self.filename}.mp3")

    def test_record_audio(self):
        """Test recording audio."""
        cli_audiorecorder.recorder(self.url, self.filename, self.duration, self.blocksize)
        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM recordings")
        count = c.fetchone()[0]
        conn.close()
        self.assertEqual(count, 1, "Recording was not saved in the database.")

    def test_list_recordings(self):
        """Test listing recordings."""
        cli_audiorecorder.recorder(self.url, self.filename, self.duration, self.blocksize)
        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()
        c.execute("SELECT * FROM recordings")
        rows = c.fetchall()
        conn.close()
        self.assertEqual(len(rows), 1, "Recording was not listed correctly.")

    def test_clear_database(self):
        """Test clearing the database."""
        cli_audiorecorder.recorder(self.url, self.filename, self.duration, self.blocksize)
        cli_audiorecorder.clear_database()
        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM recordings")
        count = c.fetchone()[0]
        conn.close()
        self.assertEqual(count, 0, "Database was not cleared.")

    def test_invalid_url(self):
        """Test handling of invalid URL."""
        with self.assertRaises(ValueError):
            cli_audiorecorder.recorder("invalid_url", self.filename, self.duration, self.blocksize)

if __name__ == '__main__':
    unittest.main()