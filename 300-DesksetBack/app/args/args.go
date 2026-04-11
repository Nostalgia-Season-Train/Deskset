package args

import (
	"flag"
)

var (
	DevMode bool
	Port    int
	Token   string
)

func init() {
	flag.BoolVar(&DevMode, "dev", false, "Enable development mode")
	flag.IntVar(&Port, "port", 6527, "Set server port")
	flag.StringVar(&Token, "token", "", "Set authentication token")
}
