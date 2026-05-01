package main

import (
	"fmt"
	"os"
)

func main() {
	args := os.Args[1:]
	cmd := "serve"
	if len(args) > 0 {
		cmd = args[0]
		args = args[1:]
	}
	switch cmd {
	case "serve":
		runServe()
	case "maintain":
		runMaintain()
	case "search":
		runSearch(args)
	default:
		fmt.Fprintf(os.Stderr, "usage: reelm [serve|maintain|search <query>]\n")
		os.Exit(1)
	}
}
