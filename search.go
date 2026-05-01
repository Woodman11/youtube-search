package main

import (
	"database/sql"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

func runSearch(args []string) {
	if len(args) == 0 || args[0] == "--help" {
		fmt.Print(`usage: reelm search [--list] [--open] <query>

  reelm search "proxmox vlan"
  reelm search "veeam backup" --open   # opens top result in browser
  reelm search --list                  # list all saved videos
`)
		return
	}

	db, err := openDB()
	if err != nil {
		fmt.Fprintf(os.Stderr, "reelm search: %v\n", err)
		os.Exit(1)
	}
	defer db.Close()

	if args[0] == "--list" {
		listVideos(db)
		return
	}

	openTop := false
	var queryParts []string
	for _, a := range args {
		if a == "--open" {
			openTop = true
		} else {
			queryParts = append(queryParts, a)
		}
	}
	if len(queryParts) == 0 {
		fmt.Fprintln(os.Stderr, "provide a search query")
		os.Exit(1)
	}
	query := strings.Join(queryParts, " ")

	rows, err := db.Query(`
		SELECT v.title, s.video_id, s.start_secs
		FROM segments s
		JOIN videos v ON v.id = s.video_id
		WHERE segments MATCH ?
		ORDER BY rank
		LIMIT 25
	`, query)
	if err != nil {
		fmt.Fprintf(os.Stderr, "search error: %v\n", err)
		os.Exit(1)
	}
	defer rows.Close()

	type result struct {
		title   string
		videoID string
		start   int
	}
	var results []result
	for rows.Next() {
		var res result
		rows.Scan(&res.title, &res.videoID, &res.start)
		results = append(results, res)
	}

	if len(results) == 0 {
		fmt.Printf("No results for: %q\n", query)
		return
	}

	fmt.Printf("\n%d result(s) for %q:\n\n", len(results), query)
	for i, res := range results {
		url := ytURL(res.videoID, res.start)
		fmt.Printf("  %2d. [%s] %s\n      %s\n\n", i+1, fmtTime(res.start), res.title, url)
	}

	if openTop {
		url := ytURL(results[0].videoID, results[0].start)
		fmt.Printf("Opening: %s\n", url)
		exec.Command("open", url).Run()
	}
}

func listVideos(db *sql.DB) {
	rows, err := db.Query(`
		SELECT id, title, save_ts_secs, has_transcript
		FROM videos
		ORDER BY indexed_at DESC
	`)
	if err != nil {
		fmt.Fprintf(os.Stderr, "list error: %v\n", err)
		os.Exit(1)
	}
	defer rows.Close()

	fmt.Printf("\n%4s  %-55s %10s  Saved at\n%s\n", "", "Title", "Transcript", strings.Repeat("-", 85))
	any := false
	for rows.Next() {
		any = true
		var id, title string
		var saveSecs, hasTr int
		rows.Scan(&id, &title, &saveSecs, &hasTr)
		tr := "no"
		if hasTr == 1 {
			tr = "yes"
		}
		fmt.Printf("       %-55s  %10s  %s\n", truncate(title, 55), tr, fmtTime(saveSecs))
		fmt.Printf("       https://youtube.com/watch?v=%s\n\n", id)
	}
	if !any {
		fmt.Println("No saved videos yet.")
	}
}

func ytURL(videoID string, startSecs int) string {
	return fmt.Sprintf("https://youtube.com/watch?v=%s&t=%d", videoID, startSecs)
}

func fmtTime(secs int) string {
	h, rem := secs/3600, secs%3600
	m, s := rem/60, rem%60
	if h > 0 {
		return fmt.Sprintf("%d:%02d:%02d", h, m, s)
	}
	return fmt.Sprintf("%d:%02d", m, s)
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return s[:n]
}
