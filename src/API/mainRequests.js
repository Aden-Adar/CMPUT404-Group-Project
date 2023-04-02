import { Buffer } from "buffer"

const AUTHOR = JSON.parse(window.localStorage.getItem("Author"))
const GROUP1URL = "https://social-distribution-w23-t17.herokuapp.com/"
const GROUP1CREDS = Buffer.from("remote-user-t22:pZHAe3PWukpd3Nv").toString('base64')
async function getExplorePosts() {
    let posts = []

    // POSTS FROM OUR BACKEND
    let authorsResponse = await fetch('/service/authors/')
    let authorsRes_data = await authorsResponse.json()
    for (let i = 0; i < authorsRes_data.items.length; i++) {
        if (authorsRes_data.items[i].id !== AUTHOR.id) {
            let authorPosts = []
            let response = await fetch(authorsRes_data.items[i].url + "posts/")
            let res_data = await response.json()
            console.log("OUR BE->", res_data)
            // Filter out any of logged in users' posts
            for (let j = 0; j < res_data.length; j++) {
                if (res_data[j].visibility === "PUBLIC") {
                    authorPosts.push(res_data[j])
                }
            }
            posts = posts.concat(authorPosts)
        }
    }
    
    // POSTS FROM GROUP 1's BE
    let authorsResponse2 = await fetch(GROUP1URL+'authors/', {
        method: 'GET',
        headers: {
            'Authorization': 'Basic ' + GROUP1CREDS,
            'Access-Control-Request-Method': 'GET' 
        }
    })
    let authorsRes_data2 = await authorsResponse2.json()
    console.log(authorsRes_data2)
    for (let i = 0; i < authorsRes_data2.items.length; i++) {
        if (authorsRes_data2.items[i].id !== AUTHOR.id) {
            let authorPosts = []
            let response = await fetch(GROUP1URL + 'authors/' + authorsRes_data2.items[i].id + '/posts/', {
                method: 'GET',
                headers: {
                    'Authorization': 'Basic ' + GROUP1CREDS,
                    'Access-Control-Request-Method': 'GET' 
                }
            })
            let res_data = await response.json()
            console.log(res_data)
            for (let j = 0; j < res_data.items.length; j++) {
                if (res_data.items[j].visibility === "PUBLIC") {
                    let commentsResponse = await fetch(GROUP1URL + 'authors/' + authorsRes_data2.items[i].id + '/posts/' + res_data.items[j].id + '/comments/', {
                        method: 'GET',
                        headers: {
                            'Authorization': 'Basic ' + GROUP1CREDS,
                            'Access-Control-Request-Method': 'GET' 
                        }
                    })
                    let commentsRes_data = await commentsResponse.json()
                    res_data.items[j].comments = commentsRes_data.id
                    res_data.items[j].comments_set = commentsRes_data.items
                    authorPosts.push(res_data.items[j])
                }
            }
            posts = posts.concat(authorPosts)
        }
    }
    return posts
}

async function getMyPosts() {
    let response = await fetch(AUTHOR.url + 'posts/')
    let res_data = await response.json()
    return res_data
}

async function getInbox() {
    let response = await fetch(AUTHOR.url + 'inbox/')
    let res_data = await response.json()
    return res_data.items
}

export {getExplorePosts, getMyPosts, getInbox}