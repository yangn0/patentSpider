package main

import (
	"context"
	"errors"
	"fmt"
	"strconv"
	"strings"
	"time"

	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"github.com/go-rod/rod/lib/proto"
	"github.com/kirinlabs/HttpRequest"
)

func handleError(err error) {
	var evalErr *rod.ErrEval
	if errors.Is(err, context.DeadlineExceeded) { // 超时异常
		fmt.Println("timeout err")
	} else if errors.As(err, &evalErr) { // eval 异常
		fmt.Println(evalErr.LineNumber)
	} else if err != nil {
		fmt.Println("can't handle", err)
	}
}

func socksproxy() (string, error) {
	req := HttpRequest.NewRequest()
	proxyurl := "http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=2&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions=&gm=4"
	res, err := req.Get(proxyurl)
	if err != nil {
		return "", err
	}
	body, err := res.Body()
	if err != nil {
		return "", err
	}
	fmt.Println(string(body))
	return string(body), nil
}

func main() {
	var browser *rod.Browser
	var page *rod.Page
	for n := 1; n < 10000; n++ {
		for {
			fmt.Println(n)
			nextPage := fmt.Sprintf("zl_fy(%s)", strconv.Itoa(n))

			// port, _ := createProxyMiddleman("socks", []string{"tps164.kdlapi.com", "20818", "t12061996266181", "tno07rxe"})
			// proxy := fmt.Sprint("localhost:%s", port)
			proxy, err := socksproxy()
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}
			url := launcher.New().
				Set("proxy-server", "socks5://"+proxy).
				MustLaunch()
			browser = rod.New().ControlURL(url).MustConnect()
			// browser = rod.New().MustConnect()
			defer browser.MustClose()
			// browser.MustIgnoreCertErrors(true)
			// go browser.MustHandleAuth("t12061996266181", "tno07rxe")()

			page, err = browser.Timeout(20 * time.Second).Page(proto.TargetCreateTarget{
				URL: "http://epub.sipo.gov.cn/gjcx.jsp?26-05",
			}) //http://epub.sipo.gov.cn/gjcx.jsp?26-05 //http://www.cip.cc/
			defer page.MustClose()
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}
			page.MustEvalOnNewDocument(`window.alert = () => {}`)

			// wait, handle := page.MustHandleDialog()
			// go page.MustElement("button").MustClick()
			// wait()
			// handle(true, "")

			_, err = page.Timeout(2000 * time.Second).Element("body > div.main > div > a:nth-child(2)")
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}
			_, err = page.Element("body > div.main > table > tbody > tr > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > span:nth-child(5) > input[checked=checked]")
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}

			wait := page.MustWaitRequestIdle()

			err = rod.Try(func() {
				page.MustEval(`patas()`)
			})
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}

			wait()

			//附图模式按钮
			_, err = page.Timeout(10 * time.Second).Element("..cp_box")
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}

			// 附图模式
			err = rod.Try(func() {
				page.MustEval(`zl_ft()`)
			})
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}
			_, err = page.Timeout(20 * time.Second).Element(".ft_cpdl2") //列表
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}
			page.MustEval(nextPage)
			_, err = page.Timeout(20 * time.Second).Element(".ft_cpdl2") //列表
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}
			var elements rod.Elements
			err = rod.Try(func() {
				elements = page.MustElements(".ft_cpdl2 strong > a")
			})
			if err != nil {
				handleError(err)
				time.Sleep(time.Second * 5)
				browser.Close()
				continue
			}
			var hrefs []string
			for _, element := range elements {
				href, _ := element.Attribute("href")
				hrefSp := strings.Split(*href, ":")[1]
				hrefs = append(hrefs, hrefSp)
			}
			fmt.Println(hrefs)
			for _, href := range hrefs {
				page.Activate()
				page.MustEval(href)
				pages, _ := browser.Pages()
				pages[0].Activate()
				err := rod.Try(func() {
					pages[0].Timeout(20 * time.Second).Element(".xmxx_tit")
				})
				if err != nil {
					handleError(err)
				}
				time.Sleep(time.Second * 2)
				pages[0].Close()
			}
			break
		}
		browser.Close()
	}
	//page.MustWaitLoad().MustScreenshot("a.png")
	time.Sleep(time.Hour)
}
