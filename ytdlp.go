package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

type segment struct {
	start float64
	text  string
}

func resolveYtdlp() (string, error) {
	if p, err := exec.LookPath("yt-dlp"); err == nil {
		return p, nil
	}
	for _, p := range []string{"/opt/homebrew/bin/yt-dlp", "/usr/local/bin/yt-dlp"} {
		if _, err := os.Stat(p); err == nil {
			return p, nil
		}
	}
	return "", fmt.Errorf("yt-dlp not found — install with `brew install yt-dlp`")
}

func fetchSegments(videoID string) ([]segment, error) {
	ytdlp, err := resolveYtdlp()
	if err != nil {
		return nil, err
	}
	tmpDir, err := os.MkdirTemp("", "reelm-*")
	if err != nil {
		return nil, err
	}
	defer os.RemoveAll(tmpDir)

	exec.Command(ytdlp,
		"--write-auto-subs",
		"--sub-lang", "en",
		"--sub-format", "json3",
		"--skip-download",
		"--no-playlist",
		"-q",
		"-o", filepath.Join(tmpDir, "%(id)s"),
		"https://www.youtube.com/watch?v="+videoID,
	).Run()

	matches, _ := filepath.Glob(filepath.Join(tmpDir, videoID+".*.json3"))
	if len(matches) == 0 {
		return nil, nil
	}
	data, err := os.ReadFile(matches[0])
	if err != nil {
		return nil, err
	}

	var j3 struct {
		Events []struct {
			TStartMs float64 `json:"tStartMs"`
			Segs     []struct {
				Utf8 string `json:"utf8"`
			} `json:"segs"`
		} `json:"events"`
	}
	if err := json.Unmarshal(data, &j3); err != nil {
		return nil, err
	}

	var segs []segment
	for _, ev := range j3.Events {
		if len(ev.Segs) == 0 {
			continue
		}
		var sb strings.Builder
		for _, s := range ev.Segs {
			sb.WriteString(s.Utf8)
		}
		text := strings.TrimSpace(sb.String())
		if text == "" || text == "\n" {
			continue
		}
		segs = append(segs, segment{start: ev.TStartMs / 1000, text: text})
	}
	return segs, nil
}
