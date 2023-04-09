// 'use strict';
const url = window.location.href
const json = JSON.stringify({'url' : url})
const link = document.createElement('a')
console.log('json: ',json)


class Candidates {

    generateCoordinates = function(item) {
        let temp_coordinates = item.getBoundingClientRect()
        return [temp_coordinates.left + window.scrollX, temp_coordinates.top + window.scrollY, temp_coordinates.right + window.scrollX, temp_coordinates.bottom + window.scrollY, temp_coordinates.height, temp_coordinates.width]
    }

    extractFeatures = function() {
        throw new Error('Cannot instantiate abstract class method.')
    }

    push = function() {
        throw new Error('Cannot instantiate abstract class method.')
    }

    makeUrlParams = function() {
        throw new Error('Cannot instantiate abstract class method.')
    }

    makeCsv = function() {
        throw new Error('Cannot instantiate abstract class method.')
    }
}

class searchCandidates extends Candidates {
    constructor (){
        super()
        this.has_inner_text = []
        this.has_search_inner_text = []
        this.num_search = []
        this.has_button = []
        this.has_search_attr = []
        this.coordinates = []
        this.extractFeatures()
    }

    push = function(item, has_inner_text, has_search_inner_text, num_search, has_button, has_search_attr) {
        console.log('search pushed: ', item, 'has_inner_text: ', has_inner_text, ' has_search_inner_text: ',has_search_inner_text, 'num_search: ', num_search, has_button, 'has_search_attr: ', has_search_attr)
        this.has_inner_text.push(has_inner_text? 1 : 0)
        this.has_search_inner_text.push(has_search_inner_text? 1 : 0)
        this.num_search.push(num_search)
        this.has_button.push(has_button? 1 : 0)
        this.has_search_attr.push(has_search_attr? 1 : 0)
        this.coordinates.push(this.generateCoordinates(item))
    }
    pop = function(){
        this.has_inner_text.pop()
        this.has_search_inner_text.pop()
        this.num_search.pop()
        this.has_button.pop()
        this.has_search_attr.pop()
        this.coordinates.pop()
    }

    

    makeUrlParams = function(){
        // Prepare the attributes into url parameters
        let inner_array_separator = ','
        let outer_array_separator = '+'
        
        let paramCoordinates = this.coordinates.map(item => item.join(inner_array_separator)) // Form string with each inner-array joined by ','
        // console.log('this.coordinates.map: ', paramCoordinates)
        paramCoordinates = paramCoordinates.join(outer_array_separator) // Form string with each item in the outer array separated by '+'
        // console.log('paramCoordinates: ', paramCoordinates)
        let paramHasInnerText = this.has_inner_text.join(outer_array_separator)
        let paramHasSearchInnerText = this.has_search_inner_text.join(outer_array_separator)
        let paramNumSearch = this.num_search.join(outer_array_separator)
        let paramHasButton = this.has_button.join(outer_array_separator)
        let paramHasSearchAttr = this.has_search_attr.join(outer_array_separator)

        let searchParam = `has_inner_text=${paramHasInnerText}&has_search_inner_text=${paramHasSearchInnerText}&num_search=${paramNumSearch}&has_button=${paramHasButton}&has_search_attr=${paramHasSearchAttr}&coordinates=${paramCoordinates}`
        
        console.log('searchParam: ',searchParam)
        return searchParam

    }

    makeCsv = function(csv_string = `has_inner_text, has_search_inner_text, num_search, has_button, has_search_attr`, filename='search_features.csv') {
        for (let i=0; i < this.has_inner_text.length; i++) {
            csv_string += `${this.has_inner_text[i]}, ${this.has_search_inner_text[i]}, ${this.num_search[i]}, ${this.has_button[i]}, ${this.has_search_attr[i]}`
        }
        var file = new Blob([json], {type : 'json'})
        link.href = URL.createObjectURL(file)
        link.download = 'search_features.csv'
        link.click()
        URL.revokeObjectURL(link.href)
        
    }

    extractFeatures = function () {
        let csv_string = ``
        for (const item of document.querySelectorAll('form')) {
            let has_search_attr = false
            let has_button = false
            let has_inner_text = false
            let has_search_inner_text = false
            let num_search = 0
            console.log('attributes: ', item.attributes)
            for (const att of item.attributes) {
                // console.log(att.value.toLowerCase())
                if (att.value.toLowerCase().match('search')) {
                    // console.log('attribute: ',att)
                    console.log('value: ',att.value)
                    has_search_attr = true
            
            // check if it has inner text (aria-label and placeholder are also considered inner text)
            if (item.attributes['aria-label'] != undefined && item.attributes['aria-label'].value.toLowerCase().match('search')) {
                has_search_inner_text = true
                num_search += 1
            }
            if (item.attributes['placeholder'] != undefined && item.attributes['placeholder'].value.toLowerCase().match('search')) {
                has_search_inner_text = true
                num_search += 1
            }
            }
            }
            for (const child of item.querySelectorAll('*')){
                for (const child_att of child.attributes) {

                    // console.log('child: ',child)
                    if (child_att.value.toLowerCase().match('search')) {
                        // console.log('child: ',child)
                        // console.log('attribute: ',child_att)
                        // console.log('value: ',child_att.value)
                        has_search_attr = true
                        
                    }
               
                }
                // Check if child has innerText
                 if (child.innerText) {
                    // console.log('child: ',child)
                    // console.log('innerText: ',child.innerText)
                    has_inner_text = true
                    if (child.innerText.toLowerCase().match('search')) {
                        console.log('child: ',child)
                        // console.log('innerText: ',child.innerText)
                        has_search_inner_text = true
                        num_search += 1
                        console.log('num_search: ', num_search)
                    }
                }
                

                if (child.attributes['aria-label'] != undefined) {
                    // console.log('child:',child)
                    // console.log('aria-label:',child.attributes['aria-label'].value)
                    has_inner_text = true
                    if (child.attributes['aria-label'].value.toLowerCase().match('search')) {
                        has_search_inner_text = true
                        num_search += 1
                    }
                }
                if (child.attributes['placeholder'] != undefined) {
                    // console.log('child:',child)
                    // console.log('placeholder:',child.attributes['placeholder'].value)
                    has_inner_text = true
                    if (child.attributes['placeholder'].value.toLowerCase().match('search')) {
                        has_search_inner_text = true
                        num_search += 1
                    }
                }
            }
        // Check for button in children
            if (item.querySelector('button')){
                // console.log('button: ',item.querySelector('button'));
                // console.log('has button: ', item.querySelector('button'))
                // console.log('has search attr: ', has_search_attr)
                has_button = true
            }
    
            if (item.querySelector('input[type = button]')){
                console.log('input button: ',item.querySelector('input[type = button]'));
                // console.log('has button: ', item.querySelector('input[type = button]'))
                // console.log('has search attr: ', has_search_attr)
                has_button = true
                
            }
            this.push(item, has_inner_text=has_inner_text, has_search_inner_text=has_search_inner_text, num_search=num_search, has_button=has_button, has_search_attr=has_search_attr)
        }   
    }
};

class filterCandidates extends Candidates {
    constructor (){
        super()
        this.has_checkbox_list = []
        this.num_links = []
        this.num_inputs = []
        this.all_child_links_valid = []
        this.has_button_list = []
        this.coordinates = []
        this.extractFeatures()
    }

    push = function(item, has_checkbox_list, num_links, num_inputs, has_button_list, all_child_links_valid) {
        // console.log('pushed: ', item, 'has_checkbox_list: ', has_checkbox_list, ' num_links: ',num_links, 'num_inputs: ', num_inputs, 'has_button_list: ',has_button_list, 'all_child_links_valid: ', all_child_links_valid)
        this.has_checkbox_list.push(has_checkbox_list? 1 : 0)
        this.num_links.push(num_links)
        this.num_inputs.push(num_inputs)
        this.has_button_list.push(has_button_list? 1 : 0)
        this.all_child_links_valid.push(all_child_links_valid? 1 : 0)
        this.coordinates.push(this.generateCoordinates(item))
    }
 

    

    makeUrlParams = function(){
        // Prepare the attributes into url parameters
        let inner_array_separator = ','
        let outer_array_separator = '+'
        
        let paramCoordinates = this.coordinates.map(item => item.join(inner_array_separator)) // Form string with each inner-array joined by ','
        console.log('this.coordinates.map: ', paramCoordinates)
        paramCoordinates = paramCoordinates.join(outer_array_separator) // Form string with each item in the outer array separated by '+'
        console.log('paramCoordinates: ', paramCoordinates)
        let paramHasCheckboxList = this.has_checkbox_list.join(outer_array_separator)
        let paramNumLinks = this.num_links.join(outer_array_separator)
        let paramNumInputs = this.num_inputs.join(outer_array_separator)
        let paramHasButtonList = this.has_button_list.join(outer_array_separator)
        let paramAllChildLinksValid = this.all_child_links_valid.join(outer_array_separator)
        let searchParam = `has_checkbox_list=${paramHasCheckboxList}&num_links=${paramNumLinks}&num_inputs=${paramNumInputs}&has_button_list=${paramHasButtonList}&all_child_links_valid=${paramAllChildLinksValid}&coordinates=${paramCoordinates}`
        
        console.log('searchParam: ',searchParam)
        return searchParam

    }

    makeCsv = function(csvString = `has_checkbox_list, num_links, num_inputs, has_button_list, all_child_links_valid\r\n`, filename='filter_features.csv') {
        for (let i=0; i < this.has_inner_text.length; i++) {
            csvString += `${this.has_checkbox_list[i]}, ${this.num_links[i]}, ${this.num_inputs[i]}, ${this.has_button_list[i]}, ${this.all_child_links_valid[i]}\r\n`
        }
        console.log(csvString)
        var file = new Blob([csvString], {type : 'text/csv;charset=utf-8;'})
        link.href = URL.createObjectURL(file)
        link.download = 'search_features.csv'
        link.click()
        URL.revokeObjectURL(link.href)
        
    }

    extractFeatures = function () {
        // function findOuterParent(element, parentElement) {
        //     let closestParentElement = $(element).closest(parentElement)
        //     let outerParentElement = $(closestParentElement).closest(parentElement)
        //     if (closestParentElement.find('*') === outerParentElement.find('* : not(nth-child(1)'))
        // }
        const elements = {
            divs : document.querySelectorAll('div > nav, div > ul, div > a, div > dl'),
            // nav : document.querySelectorAll('nav'),
            // li : document.querySelectorAll('li'),
            // ul : document.querySelectorAll('ul'),
            span : document.querySelectorAll('span > nav, span > a, span > ul, span > dl'),
            section : document.querySelectorAll('section > nav, section > ul, section > dl'),
            form : document.querySelectorAll('form')
            // button : document.querySelectorAll('button'),
            // tr : document.querySelectorAll('tr'),
            // footer : document.querySelectorAll('footer'),
            // a : document.querySelectorAll('a'),
            // pagination : document.querySelectorAll('pagination'),
            // b : document.querySelectorAll('b')
        }

        for (const element in elements) {
            console.log('element: ',elements[element],' elements: ',elements)
            for (const item of elements[element]) {
                let has_checkbox_list = false
                let num_links = 0
                let num_inputs = 0
                let all_child_links_valid = true
                let has_button_list = false

                // has_checkbox_list
                if (item.querySelectorAll('input[type=checkbox]').length > 1) {
                    has_checkbox_list = true
                }
                // num_links
                num_links = item.querySelectorAll('a').length

                // all_child_links_valid
                for (const a of item.querySelectorAll('a')) {
                    if (!a.getAttribute('href')) {
                        all_child_links_valid = false
                    }
                }

                // num_inputs
                num_inputs = item.querySelectorAll('input').length

                // has_button_list
                if (item.querySelectorAll('button').length > 1 || item.querySelectorAll('input[type=button]').length > 1 || item.querySelectorAll('input[type=submit]').length > 1) {
                    has_button_list = true
                }
                this.push(item, has_checkbox_list=has_checkbox_list, num_links=num_links, num_inputs=num_inputs, has_button_list=has_button_list, all_child_links_valid=all_child_links_valid)
            }
        }
    }
};

class sortCandidates extends Candidates {
    
    constructor() {
        super()
        this.keyword_match = []
        this.keyword_count = []
        this.has_sort_text = []
        this.num_option_tag = []
        this.coordinates = []
        this.extractFeatures()
    }

    push = function(item, keyword_match, keyword_count, has_sort_text, num_option_tag) {
        console.log('sort pushed: ',keyword_match,' ',keyword_count,' ',has_sort_text,' ',num_option_tag)
        this.keyword_match.push(keyword_match)
        this.keyword_count.push(keyword_count)
        this.has_sort_text.push(has_sort_text)
        this.num_option_tag.push(num_option_tag)
        this.coordinates.push(this.generateCoordinates(item))
    }

    extractFeatures = function() {

        
        const keywords = ['price', 'recommended', 'ratings', 'distance','time', 'most recent', 'best match', 'relevance', 'featured', 'new', 'highest']

        
        for (const item of document.querySelectorAll('select, ul')) {
            let keyword_match = false
            let keyword_count = 0
            let has_sort_text = false
            let num_option_tag = 0
            // check inner text for keywords: price, recommended, ratings, distance, time
            console.log('sort item: ',item)
            // keyword_count = item.querySelectorAll('*: contains("Price" i), * : contains("Recommended" i), * : contains("Ratings" i), * : contains("Distance" i), * : contains("Time" i), * : contains("Most Recent" i), * : contains("Best Match" i), * : contains("Relevance" i), * : contains("Featured" i), * : contains("New" i), * : contains("Highest" i)').length
            for (const inner_item of item.querySelectorAll('*')) {
                if (keywords.includes(inner_item.innerText.toLowerCase())) {
                    keyword_count += 1
                }

                // has_sort_text
                if (inner_item.innerText.toLowerCase() === "sort") {
                    has_sort_text = true
                }
            }
            // keyword_match
            keyword_match = keyword_count > 0
            // for (const inner_item of item.querySelectorAll('*')){
            //     if (inner_item.innerText.toLowerCase() === "sort") {
            //         has_sort_text = true
            //         break
            //     }
            // }
            num_option_tag = item.querySelectorAll('li').length
            this.push(item, keyword_count=keyword_count, keyword_match=keyword_match, has_sort_text=has_sort_text, num_option_tag=num_option_tag)
        }
    }
}

class pageCandidates extends Candidates {
    constructor() {
        this.num_buttons = []
        this.num_links = []
        this.num_common_url = []
        this.num_numeric_nodes = [] // no. of nodes with only numbers as text
        this.has_keyword = []
        this.keyword_count = []
        this.coordinates = []
    }

    push = function(item, num_buttons, num_links, num_common_url, num_numeric_nodes, has_keyword, keyword_count) {
        this.num_buttons.push(num_buttons)
        this.num_links.push(num_links)
        this.num_common_url.push(num_common_url)
        this.num_numeric_nodes.push(num_numeric_nodes)
        this.has_keyword.push(has_keyword)
        this.keyword_count.push(keyword_count)
        this.coordinates.push(generateCoordinates(item))
    }

    extractFeatures = function() {
        for (const item of document.querySelectorAll('')) {
            let num_buttons = 0
            let num_links = 0
            let num_common_url = 0
            let num_numeric_nodes = 0
            let has_keyword = false
            let keyword_count = 0
            
        }
    }
}
const searchCandidateList = new searchCandidates()
// const filterCandidateList = new filterCandidates()
const sortCandidateList = new sortCandidates()

data = {
    search : searchCandidateList,
    // filter : filterCandidateList,
    sort : sortCandidateList,
    // viewport size
    viewport_width : window.innerWidth,
    viewport_height : window.innerHeight,
    //document size
    page_width : document.documentElement.getBoundingClientRect().width,
    page_height : document.documentElement.getBoundingClientRect().height

}

console.log('data output: ',JSON.stringify(data))
console.log('search output: ',JSON.stringify(searchCandidateList))
// console.log('filter output: ',JSON.stringify(filterCandidateList))
console.log('sort output: ',JSON.stringify(sortCandidateList))

// searchCandidateList.makeCsv()
// filterCandidatesList.makeCsv()
// extractFeatures()
// console.log(searchCandidateList)
// var file = new Blob([json], {type : 'json'})
// link.href = URL.createObjectURL(file)
// link.download = 'features.json'
// link.click()
// URL.revokeObjectURL(link.href)


// replace data with the objects to be sent
fetch('http://127.0.0.1:5000/generate_summary/', {method: 'POST', headers: {"content-Type" : "application/json"}, body: JSON.stringify(data)}).then(response => response.text).then(result => console.log('fetch result: ',result)).catch(error => console.log('error', error))