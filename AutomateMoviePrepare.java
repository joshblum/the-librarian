import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.Map.Entry;

public class AutomateMoviePrepare {
	String FFMPEG_DIR = "";
	
	public static String pathJoin(String path1, String path2) {
		File file1 = new File(path1);
		File file2 = new File(file1, path2);
		return file2.getPath();
	}
	
	
	public static void makeMPFromDir(String path, String framerate, String bitrate, String channels) {
		File dir = new File(path);
		for (File c : dir.listFiles()) {
			makeAllStreams(c.getAbsolutePath(), framerate, bitrate, channels);
		}
	}

	public static void makeAllStreams(String filename, String framerate, String bitrate, String channels) {
		Map<String, String> streams = getStreams(filename);
		for (Entry<String, String> st : streams.entrySet()) {
			makeMP3Stream(filename, st.getKey(), st.getValue(), framerate, bitrate, channels);
		}
	}

	public static void makeMP3Stream(String filename, String stream, String lang, String framerate, String bitrate,
			String channels) {
		List<String> commands = new ArrayList<String>();
		String ffmpegPath = pathJoin(FFMPEG_DIR, "ffmpeg.exe");
		String newFileName = new File(filename).getAbsolutePath().split("\\.")[0] + " " + lang;
		commands.addAll(Arrays.asList(new String[] { ffmpegPath, "-y", "-i", filename, "-acodec", "libmp3lame", "-map",
				stream }));
		if (framerate.equals("-1") == false) {
			commands.add("-r:a");
			commands.add(framerate);
			newFileName += " f-" + framerate;
		}
		if (bitrate.equals("-1") == false) {
			commands.add("-b:a");
			commands.add(bitrate);
			newFileName += " b-" + bitrate;
		}
		if (channels.equals("-1") == false) {
			commands.add("-ac");
			commands.add(channels);
		}
		newFileName += ".mp3";

		commands.add(newFileName);
		ProcessBuilder builder = new ProcessBuilder(commands);
		builder.directory(new File(FFMPEG_DIR));
		builder.redirectErrorStream(true);
		try {
			Process proc = builder.start();
			BufferedReader reader = new BufferedReader(new InputStreamReader(proc.getInputStream()));
			String line;
			while ((line = reader.readLine()) != null) {
			}
			proc.waitFor();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}

	public static Map<String, String> getStreams(String filename) {
		Map<String, String> retVal = new TreeMap<String, String>();

		String ffmpegPath = pathJoin(FFMPEG_DIR, "ffmpeg.exe");
		ProcessBuilder builder = new ProcessBuilder(ffmpegPath, "-i", filename);
		builder.directory(new File(FFMPEG_DIR));
		builder.redirectErrorStream(true);
		String streamPart = null, streamName = null;
		try {
			Process proc = builder.start();
			BufferedReader reader = new BufferedReader(new InputStreamReader(proc.getInputStream()));
			String line;
			while ((line = reader.readLine()) != null) {
				System.out.println(line);
				if (line.contains("Stream") && line.contains("Audio")) {
					String splited = line.split("#")[1].split("\\s+")[0];
					if (splited.contains("(") == true) {
						streamPart = splited.split("\\(")[0];
						streamName = splited.split("\\(")[1].split("\\)")[0];
					} else {
						streamPart = splited.substring(0, splited.length() - 1);
						streamName = "unknown" + streamPart.split(":")[1];
					}

					retVal.put(streamPart, streamName);
				}
			}
		} catch (IOException e) {
			return null;
		}
		return retVal;
	}
}
