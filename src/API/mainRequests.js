import { Buffer } from "buffer"

const AUTHOR = JSON.parse(window.localStorage.getItem("Author"))

const GROUP1URL = "https://social-distribution-w23-t17.herokuapp.com/"
const GROUP1CREDS = Buffer.from("remote-user-t22:pZHAe3PWukpd3Nv").toString('base64')

const GROUP2URL = "https://floating-fjord-51978.herokuapp.com/"
const GROUP2CREDS = Buffer.from("admin:admin").toString('base64')
async function getExplorePosts(page) {
    let posts = []

    // // POSTS FROM OUR BACKEND
    try {
        let authorsResponse = await fetch(`/service/authors/?page=${page}&count=3`)
        let authorsRes_data = await authorsResponse.json()
        for (let i = 0; i < authorsRes_data.items.length; i++) {
            if (!authorsRes_data.items[i].id.includes(GROUP1URL) && !authorsRes_data.items[i].id.includes(GROUP2URL) && authorsRes_data.items[i].id !== AUTHOR.id) {
                let authorPosts = []
                let response = await fetch(authorsRes_data.items[i].url + "posts/")
                let res_data = await response.json()
                // Filter out any of logged in users' posts
                for (let j = 0; j < res_data.length; j++) {
                    if (res_data[j].visibility === "PUBLIC") {
                        authorPosts.push(res_data[j])
                    }
                }
                posts = posts.concat(authorPosts)
            }
        }
    } catch (error) {
        console.log(error)
    }
    
    // // POSTS FROM GROUP 1's BE
    try {
        let authorsResponse2 = await fetch(GROUP1URL+`authors/?page=${page}&size=3`, {
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
                    res_data.items[j].comments = GROUP1URL + 'authors/' + authorsRes_data2.items[i].id + '/posts/' + res_data.items[j].id + '/comments/'
                    authorPosts.push(res_data.items[j])
                }
                posts = posts.concat(authorPosts)
            }
        }
    } catch (error) {
        console.log(error)
    }

    // POSTS FROM GROUP 2's BE
    try {
        let authorsResponse3 = await fetch(GROUP2URL+`authors/?page=${page}&size=5`, {
            method: 'GET',
            headers: {
                'Authorization': 'Basic ' + GROUP2CREDS,
                'Access-Control-Request-Method': 'GET' 
            }
        })
        let authorsRes_data3 = await authorsResponse3.json()
        for (let i = 0; i < authorsRes_data3.items.length; i++) {
            console.log("original post: ", authorsRes_data3.items[i]);
            if ((authorsRes_data3.items[i].id !== AUTHOR.id) && (authorsRes_data3.items[i].host === "https://floating-fjord-51978.herokuapp.com")) {
                let authorPosts = []
                let response = await fetch(authorsRes_data3.items[i].id + '/posts/', {
                    method: 'GET',
                    headers: {
                        'Authorization': 'Basic ' + GROUP2CREDS,
                        'Access-Control-Request-Method': 'GET' 
                    }
                })
                let res_data = await response.json()
                console.log(res_data)
                for (let j = 0; j < res_data.items.length; j++) {
                    res_data.items[j].comments = res_data.items[j].id + '/comments'
                    
                    authorPosts.push(res_data.items[j])
                }
                console.log("authorPosts: ", authorPosts)
                posts = posts.concat(authorPosts)
            }
        }
    } catch (error) {
        console.log(error)
    }


    return posts
}

async function getMyPosts(page) {
    let response = await fetch(AUTHOR.url + `posts/?page=${page}&count=5`)
    let res_data = await response.json()
    return res_data
}

async function getInbox() {
    let response = await fetch(AUTHOR.url + 'inbox/')
    let res_data = await response.json()
    return res_data.items
}

export {getExplorePosts, getMyPosts, getInbox}