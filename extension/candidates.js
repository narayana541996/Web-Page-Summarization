// 'use strict';
const url = window.location.href
const json = JSON.stringify({'url' : url})
const link = document.createElement('a')
console.log('json: ',json)
// import searchCandidates from "./candidates.js"
// var file = new Blob([json], {type : 'json'})
// link.href = URL.createObjectURL(file)
// link.download = 'url.json'
// link.click()
// URL.revokeObjectURL(link.href)

// extract the features, load in an array and send them as url arguments
// make a searchCandidates object and store the features

class searchCandidates {
    constructor (){
        this.has_inner_text = []
        this.has_search_inner_text = []
        this.num_search = []
        this.has_button = []
        this.has_search_attr = []
        this.coordinates = []
        this.extract_search_features()
    }

    push(item, has_inner_text, has_search_inner_text, num_search, has_button, has_search_attr){
        console.log('pushed: ', item, 'has_inner_text: ', has_inner_text, ' has_search_inner_text: ',has_search_inner_text, 'num_search: ', num_search, has_button, 'has_search_attr: ', has_search_attr)
        this.has_inner_text.push(has_inner_text? 1 : 0)
        this.has_search_inner_text.push(has_search_inner_text? 1 : 0)
        this.num_search.push(num_search)
        this.has_button.push(has_button? 1 : 0)
        this.has_search_attr.push(has_search_attr? 1 : 0)
        this.coordinates.push(this.generateCoordinates(item))
    }
    pop(){
        this.has_inner_text.pop()
        this.has_search_inner_text.pop()
        this.num_search.pop()
        this.has_button.pop()
        this.has_search_attr.pop()
        this.coordinates.pop()
    }

    generateCoordinates(item) {
        let temp_coordinates = item.getBoundingClientRect()
        return [temp_coordinates.left + window.scrollX, temp_coordinates.top + window.scrollY, temp_coordinates.right + window.scrollX, temp_coordinates.bottom + window.scrollY, temp_coordinates.height, temp_coordinates.width]
    }

    makeUrlParams(){
        // Prepare the attributes into url parameters
        let inner_array_separator = ','
        let outer_array_separator = '+'
        
        let paramCoordinates = this.coordinates.map(item => item.join(inner_array_separator)) // Form string with each inner-array joined by ','
        console.log('this.coordinates.map: ', paramCoordinates)
        paramCoordinates = paramCoordinates.join(outer_array_separator) // Form string with each item in the outer array separated by '+'
        console.log('paramCoordinates: ', paramCoordinates)
        let paramHasInnerText = this.has_inner_text.join(outer_array_separator)
        let paramHasSearchInnerText = this.has_search_inner_text.join(outer_array_separator)
        let paramNumSearch = this.num_search.join(outer_array_separator)
        let paramHasButton = this.has_button.join(outer_array_separator)
        let paramHasSearchAttr = this.has_search_attr.join(outer_array_separator)
        let searchParam = `has_inner_text=${paramHasInnerText}&has_search_inner_text=${paramHasSearchInnerText}&num_search=${paramNumSearch}&has_button=${paramHasButton}&has_search_attr=${paramHasSearchAttr}&coordinates=${paramCoordinates}`
        
        console.log('searchParam: ',searchParam)
        return searchParam

    }

    extract_search_features = function () {
        'Checks if there is a search keyword in attribute values.'
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

                    console.log('child: ',child)
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
                    console.log('child:',child)
                    console.log('aria-label:',child.attributes['aria-label'].value)
                    has_inner_text = true
                    if (child.attributes['aria-label'].value.toLowerCase().match('search')) {
                        has_search_inner_text = true
                        num_search += 1
                    }
                }
                if (child.attributes['placeholder'] != undefined) {
                    console.log('child:',child)
                    console.log('placeholder:',child.attributes['placeholder'].value)
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
class filterCandidates {
    constructor (){
        this.has_checkbox_list = []
        this.num_links = []
        this.num_inputs = []
        this.all_child_links_valid = []
        this.has_button_list = []
        this.coordinates = []
        this.extract_filter_features()
    }

    push(item, has_inner_text, has_search_inner_text, num_search, has_button, has_search_attr){
        console.log('pushed: ', item, 'has_inner_text: ', has_inner_text, ' has_search_inner_text: ',has_search_inner_text, 'num_search: ', num_search, has_button, 'has_search_attr: ', has_search_attr)
        this.has_checkbox_list.push(has_checkbox_list? 1 : 0)
        this.has_search_inner_text.push(has_search_inner_text? 1 : 0)
        this.num_search.push(num_search)
        this.has_button.push(has_button? 1 : 0)
        this.has_search_attr.push(has_search_attr? 1 : 0)
        this.coordinates.push(this.generateCoordinates(item))
    }
    pop(){
        this.has_inner_text.pop()
        this.has_search_inner_text.pop()
        this.num_search.pop()
        this.has_button.pop()
        this.has_search_attr.pop()
        this.coordinates.pop()
    }

    generateCoordinates(item) {
        let temp_coordinates = item.getBoundingClientRect()
        return [temp_coordinates.left + window.scrollX, temp_coordinates.top + window.scrollY, temp_coordinates.right + window.scrollX, temp_coordinates.bottom + window.scrollY, temp_coordinates.height, temp_coordinates.width]
    }

    makeUrlParams(){
        // Prepare the attributes into url parameters
        let inner_array_separator = ','
        let outer_array_separator = '+'
        
        let paramCoordinates = this.coordinates.map(item => item.join(inner_array_separator)) // Form string with each inner-array joined by ','
        console.log('this.coordinates.map: ', paramCoordinates)
        paramCoordinates = paramCoordinates.join(outer_array_separator) // Form string with each item in the outer array separated by '+'
        console.log('paramCoordinates: ', paramCoordinates)
        let paramHasInnerText = this.has_inner_text.join(outer_array_separator)
        let paramHasSearchInnerText = this.has_search_inner_text.join(outer_array_separator)
        let paramNumSearch = this.num_search.join(outer_array_separator)
        let paramHasButton = this.has_button.join(outer_array_separator)
        let paramHasSearchAttr = this.has_search_attr.join(outer_array_separator)
        let searchParam = `has_inner_text=${paramHasInnerText}&has_search_inner_text=${paramHasSearchInnerText}&num_search=${paramNumSearch}&has_button=${paramHasButton}&has_search_attr=${paramHasSearchAttr}&coordinates=${paramCoordinates}`
        
        console.log('searchParam: ',searchParam)
        return searchParam

    }

    extract_filter_features = function () {
        'Checks if there is a search keyword in attribute values.'
        const elements = {
            divs : document.querySelectorAll('div'),
            nav : document.querySelectorAll('nav'),
            li : document.querySelectorAll('li'),
            ul : document.querySelectorAll('ul'),
            span : document.querySelectorAll('span'),
            section : document.querySelectorAll('section'),
            button : document.querySelectorAll('button'),
            tr : document.querySelectorAll('tr'),
            footer : document.querySelectorAll('footer'),
            a : document.querySelectorAll('a'),
            pagination : document.querySelectorAll('pagination'),
            b : document.querySelectorAll('b')
        }

        for (const element in elements) {
            for (const item in element) {
                let has_checkbox_list = false
                let num_links = 0
                let num_inputs = 0
                let has_url_list = false
                let has_button_list = false

                // has_checkbox_list
                if (item.querySelectorAll('input[type=checkbox]').length > 1) {
                    has_checkbox_list = true
                }
                // num_links
                num_links = element.querySelectorAll('a').length
                // has_url_list
                if (num_links > 1) {
                    has_url_list = true
                }

                // num_inputs
                num_inputs = element.querySelectorAll('input').length

                // has_button_list
                if (element.querySelectorAll('button').length > 1 || element.querySelectorAll('input[type=button]').length > 1 || element.querySelectorAll('input[type=submit]').length > 1) {
                    has_button_list = true
                }
            }
        }
    }
};

console.log('document title: ', document.title)

const searchCandidateList = new searchCandidates()

// viewport size
viewport_width = window.innerWidth
viewport_height = window.innerHeight

//document size
page_dims = document.documentElement().getBoundingClientRect()
page_width = page_dims.width
page_height = page_dims.height
console.log('page_dims: ',page_dims)

// extract_search_features()
console.log(searchCandidateList)
fetch('http://127.0.0.1:5000/generate_summary?'+searchCandidateList.makeUrlParams()+'&viewport_width='+viewport_width+'&viewport_height='+viewport_height+'&page_width='+page_width+'&page_height=',page_height).then(response => response.text).then(result => console.log(result)).catch(error => console.log('error', error))