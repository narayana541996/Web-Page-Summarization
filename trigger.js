const url = window.location.href
const json = JSON.stringify({'url' : url})
const link = document.createElement('a')
console.log('json: ',json)

// var file = new Blob([json], {type : 'json'})
// link.href = URL.createObjectURL(file)
// link.download = 'url.json'
// link.click()
// URL.revokeObjectURL(link.href)

fetch('http://127.0.0.1:5000/trigger').then(response => response.text).then(result => console.log(result)).catch(error => console.log('error', error))