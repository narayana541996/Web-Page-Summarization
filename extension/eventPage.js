chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    console.log('new page loaded: ',changeInfo, tab)
    if (changeInfo.status == "complete") {
        chrome.tabs.sendMessage(tabs[0].id, {
            todo: "NewPageLoaded"
        })

    }
})