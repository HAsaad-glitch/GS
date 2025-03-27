import requests
# ----- 1. LinkedIn Tracking Pixel Request -----
linkedin_url = "https://px.ads.linkedin.com/wa/"
linkedin_headers = {
    "accept": "*/*",
    "content-type": "text/plain;charset=UTF-8",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Referer": "https://www.referenceusa.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}
linkedin_payload = {
    "pids": [297266],
    "scriptVersion": 199,
    "time": 1742600811760,
    "domain": "referenceusa.com",
    "url": "https://referenceusa.com/UsBusiness/Search/Custom/13f2b3aedb29457490db28c7337c8772",
    "pageTitle": "U.S. Businesses - Advanced Search | Data Axle Reference Solutions",
    "websiteSignalRequestId": "4c698a1f-8d0c-47cb-15a6-b8d77b182d24",
    "isTranslated": False,
    "liFatId": "",
    "liGiant": "",
    "misc": {"psbState": -4},
    "isLinkedInApp": False,
    "hem": None,
    "signalType": "CLICK",
    "href": "#",
    "domAttributes": {
        "elementSemanticType": None,
        "elementValue": None,
        "elementType": None,
        "tagName": "A",
        "backgroundImageSrc": "https://www.referenceusa.com/Themes/Default/Content/Images/SearchInterface/Shared/Grn_button_medium_127x48_Hover_New.png",
        "imageSrc": None,
        "imageAlt": None,
        "innerText": "VIEW RESULTS",
        "elementTitle": None,
        "cursor": "pointer"
    },
    "innerElements": None,
    "elementCrumbsTree": [
        {"tagName": "div", "nthChild": 4, "id": "container"},
        {"tagName": "div", "nthChild": 0, "classes": ["contentLeftEdge"]},
        {"tagName": "div", "nthChild": 0, "classes": ["contentRightEdge"]},
        {"tagName": "div", "nthChild": 0, "classes": ["pageArea"]},
        {"tagName": "div", "nthChild": 2, "id": "content"},
        {"tagName": "div", "nthChild": 0, "id": "search"},
        {"tagName": "div", "nthChild": 0, "id": "searchInterface"},
        {"tagName": "div", "nthChild": 1, "id": "dbSelector"},
        {"tagName": "div", "nthChild": 0, "classes": ["clear", "content"]},
        {"tagName": "div", "nthChild": 2, "classes": ["clear", "innerContent"]},
        {"tagName": "div", "nthChild": 0, "classes": ["contain-enterkey", "customSearchContainer"]},
        {"tagName": "div", "nthChild": 2, "classes": ["summaryColumn"]},
        {"tagName": "div", "nthChild": 0, "classes": ["resultsSummary", "vertical-scroll-with"]},
        {
            "tagName": "a",
            "nthChild": 0,
            "classes": ["action-view-results", "greenMedium", "standardButtons"],
            "attributes": {"href": "#"}
        }
    ],
    "isFilteredByClient": False
}
linkedin_response = requests.post(
    linkedin_url,
    headers=linkedin_headers,
    json=linkedin_payload
)
print("LinkedIn response:", linkedin_response.status_code)
# ----- 2. ReferenceUSA Business Search Request -----
search_url = "https://www.referenceusa.com/UsBusiness/Search/NewCustomSearchRequest/13f2b3aedb29457490db28c7337c8772"
search_headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "request-context": "appId=cid-v1:6f5cad55-8123-4589-8d6d-e647a71d2872",
    "request-id": "|46ae78d24f2b4a62a7f3ee5f8ba1109c.1e59224e22714540",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Microsoft Edge\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "traceparent": "00-46ae78d24f2b4a62a7f3ee5f8ba1109c-1e59224e22714540-01",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "https://www.referenceusa.com/UsBusiness/Search/Custom/13f2b3aedb29457490db28c7337c8772",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "cookie": """ai_user=Pkk0Jls6m3Y45X7kiDhqjH|2025-03-15T06:50:04.455Z; hubspotutk=0107917c0ef85668bf29dd33b1b559a3; ASP.NET_SessionId=yioqepjlllpujlsizq5l5xeu; LoginToken=10138b67-1707-4d4a-b669-2c20339d4084; TS01d981e1=01065b9f50ed63b33dd6e814aa0a72b5ff17469337a39e30a55c54d0aa2488655abbed3f73a3f4aec0675f7472dfdd8896c1364236; __utmc=72359952; __utmz=72359952.1742418950.5.3.utmcsr=web.ocpl.org|utmccn=(referral)|utmcmd=referral|utmcct=/db/refusa/; UserAuthenticated=true; __hssrc=1; ASP.NET_SessionID=; .ASPXAUTH=C0B5D9A2BC0FAC236FD863D30BF286F5373DA181F14CDD48EE8724FA6A994191AFF92880E01895AC43AE0287A0527C3FA2F417EE5FB5471EB2019A69BF3876D33799855BED3A7C50029EDC1DFA474F26E282957EEC8F8F4DE14AD1D896C50CC16FF7BA1BEB9A85DEB039CDDD3B8893DCA2870E0659C5CB157E9B72EB12BE44D201A080059C626136EC496CB6410BF3011FE16D65365E24101F91B7634E2E3B0FA903E61AE206665791D3BD7FBDF854B4B4ACA644F672D2E47DA16E1A5322E162B5C1D355230B38077740DE668F8E55F3CB8003B6C03C9F31592056FBD4A23B30B8193F38164337121A3866AD6CBE9E1CA8024224D9B188911EB8D1A57DC92DC01338CF0502AD033CE76A96FC0E4B625D3BB0F02EA5161ADA0EF97C606EBF6CFBFAD0A0985EEE3C78F4AB9B5B25D3D91A9FE7F2BFB83055AD1C3ACA5D5C5CBFAAD8733904EFC3534C89D418B064444D34CDBD9B42A1A15DB0750FEEC4072AD2D9A6D9C779CE62546D5724954AB357EB2432BC449D67E668A569B854863F675A059FF1A208B11BA78960FFF3B48F3A3DEFE7BD399C40D6FA44E8106739571E8E1040DA53AA5F6B435B03034E11D8F78DC707B13FA7FBD042A71129F9337748400937E24717989DAB88B803C7A1A24AFC4F6DA813377C9652CA41033FADBC559F2788586BC2784F64610044A5956F20078DE441839CB4D80CC53E9BEAF903B14270D5A2E64851ADDF543A11EF3882BC5A02C02F363295C50EC96F74A8B8B1F374F8D2E8527C3DE4C351"""
}
search_payload = "VerifiedRecord=V&PrimarySic=&PrimarySicLookup=&Sic=&SicLookup=&Naics=&NaicsLookup=&PrimaryNaicsLookup=62139901&PrimaryNaics=&postbackType=viewresults"
search_response = requests.post(
    search_url,
    headers=search_headers,
    data=search_payload
)
print("Search response:", search_response.status_code)
print("Search body (truncated):", search_response.text[:1000])  # Preview only first 1000 chars