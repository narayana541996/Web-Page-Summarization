// class searchCandidates {
//     constructor (){
//         this.has_inner_text = []
//         this.has_search_inner_text = []
//         this.num_search = []
//         this.has_button = []
//         this.has_search_attr = []
//         this.coordinates = []
//     }

//     push(item, has_inner_text, has_search_inner_text, num_search, has_button, has_search_attr){
//         console.log('pushed: ',item, has_inner_text, has_search_inner_text, num_search, has_button, has_search_attr)
//         this.has_inner_text.push(has_inner_text)
//         this.has_search_inner_text.push(has_search_inner_text)
//         this.num_search.push(num_search)
//         this.has_button.push(has_button)
//         this.has_search_attr.push(has_search_attr)
//         this.coordinates.push(this.generateCoordinates(item))
//     }
//     pop(){
//         this.has_inner_text.pop()
//         this.has_search_inner_text.pop()
//         this.num_search.pop()
//         this.has_button.pop()
//         this.has_search_attr.pop()
//         this.coordinates.pop()
//     }

//     generateCoordinates(item) {
//         let temp_coordinates = item.getBoundingClientRect()
//         return [temp_coordinates.left, temp_coordinates.top, temp_coordinates.right, temp_coordinates.bottom, temp_coordinates.height, temp_coordinates.width]
//     }
// };

// // export default searchCandidates;