import * as React from 'react';
import { Buffer } from "buffer"
import { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Checkbox from '@material-ui/core/Checkbox';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import axios from 'axios';


const useStyles = makeStyles((theme) => ({

  formControl: {
    minHeight: 120,
    minWidth: 120
  },

  selectEmpty: {
    marginTop: theme.spacing(5),
    marginRight: theme.spacing(5)
  },
  checkbox: {
    marginTop: theme.spacing(4),
    marginRight: theme.spacing(2)
  },
  textField: {
    marginTop: theme.spacing(10),
    marginBottom: theme.spacing(10)
  },
  container: {
    display: 'flex',
    justifyContent: 'space-between', 
    alignItems: 'flex-end', 
    marginBottom: theme.spacing(5) 
  },
  button: {
    padding: theme.spacing(5), 
    marginLeft: 'auto', 
    marginBottom: theme.spacing(5),
  },
  header: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(5),
    fontWeight: 'bold',
    fontSize: '32pt',
    textAlign: 'center',
  }
}));


function CreatePost()  {
  const classes = useStyles();
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [content_type, setContentType] = useState('');
  const [content, setContent] = useState('');
  const [visibility, setVisibility] = useState('');
  const [unlisted, setUnlisted] = useState(false);
  const [categories, setCategories] = useState([]);
  const [file, setFile] = useState(null);
  const [followers, setFollowers] = useState([]);
  const author = JSON.parse(window.localStorage.getItem("Author"));
  const AUTHOR_ID = author.id;

  const GROUP1URL = "https://social-distribution-w23-t17.herokuapp.com/"
  const GROUP1CREDS = Buffer.from("remote-user-t22:pZHAe3PWukpd3Nv").toString('base64')

  const GROUP2URL = "https://floating-fjord-51978.herokuapp.com/"
  const GROUP2CREDS = Buffer.from("admin:admin").toString('base64')

  useEffect(() => {
    const fetchFollowers = async () => {
      const response = await axios.get(AUTHOR_ID+'followers/');
      setFollowers(response.data.items);
    };
    
    fetchFollowers();
  }, [AUTHOR_ID]);  

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setFile(file);
  };

  
  const handleSubmit = async (event) => {
    event.preventDefault();
  
    const postData = {
      title: title,
      description: description,
      content_type: content_type,
      content: content,
      visibility: visibility,
      unlisted: unlisted,
      categories: categories,
    };

    let base64Image = '';
    if (file) {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        base64Image = reader.result.replace(/^data:image\/(png|jpeg);base64,/, '');
        postData.content = base64Image;
        setContent(base64Image);
        handlePostSubmit(postData)
      };
    } else {
      handlePostSubmit(postData)
    }
  };
    const handlePostSubmit = async (postData) =>  {
    if (visibility === "PUBLIC") {
      try {
        const response = await axios.post(AUTHOR_ID+'posts/', JSON.stringify(postData),{
          headers:{'Content-Type': 'application/json'}
        });
        console.log(response.data);
        for (let i = 0; i < followers.length; i++) {
          if (followers[i].id.includes(GROUP1URL)) {
            let postBody = response.data
            delete postBody.count;
            delete postBody.post_id;
            postBody.contentType = postBody.content_type;
            delete postBody.content_type;
            try {
              let post_res = await axios.post(GROUP1URL + `authors/${followers[i].id}inbox/`,JSON.stringify(postBody),{
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json',
                  'Authorization': 'Basic ' + GROUP1CREDS,
                  'Access-Control-Request-Method': 'POST' 
                },
              });
            } catch (error) {
              console.log(error)
            }
          }
        }
      } catch (error) {
        console.error(error);
      }
    } 
    else if (visibility === "FRIENDS") {
      try {
        const followersResponse = await axios.get(AUTHOR_ID+'followers/');
        console.log('followers:',followersResponse)
        const friends = followersResponse.data.items.map(item => item.id);
        console.log('friends:', friends);
        postData.unlisted = true;
        const publicResponse = await axios.post(AUTHOR_ID+'posts/', JSON.stringify(postData),{
          headers:{'Content-Type': 'application/json'}
        });
        console.log('mypost:',publicResponse.data);
        const friendResponse = publicResponse.data;

        for (const friend of friends) {
          try {
            console.log('friend:',friend);
            const response = await axios.post(friend+'inbox/', friendResponse,{
              headers:{'Content-Type': 'application/json'}
          });
            console.log('friend post:',response.data);
          } catch (error) {
            console.error(error);
          }
        }
      } catch (error) {
        console.error(error);
      }
      
  
        
    } 
    else if (visibility === "PRIVATE") {
      const authorName = prompt("Please enter the username of the recipient:");
  
      try {
        const authorsResponse = await axios.get('/service/authors/');
        console.log('authors:' ,authorsResponse);
        const private_author = authorsResponse.data.items.find((item) => item.displayName === authorName);
        postData.unlisted = true;
        const publicResponse = await axios.post(AUTHOR_ID+'posts/', JSON.stringify(postData),{
          headers:{'Content-Type': 'application/json'}
        });
        console.log('mypost:',publicResponse.data);
        try {
          const response = await axios.post(private_author.id+'inbox/', publicResponse.data,{
            headers:{'Content-Type': 'application/json'}
          });
          console.log('private post:',response.data);
        } catch (error) {
          console.error(error);
        }

       
      } catch (error) {
        console.error(error);
      }
    }
    window.location.href = '/main';
  };
    

  return (
    <form onSubmit={handleSubmit}>
      <Typography variant="h1" className={classes.header}>
        Create Your Post
      </Typography>
      <TextField
        required
        fullWidth
        label="Title"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
      />
      <TextField
        required
        fullWidth
        label="Description"
        value={description}
        onChange={(event) => setDescription(event.target.value)}
      />
      <TextField
        required
        fullWidth
        label="Categories (separated by commas)"
        value={categories}
        onChange={(event) => setCategories(event.target.value.split(","))}
      />
      <FormControl className={classes.formControl}>
        <Select
          required
          value={content_type}
          onChange={(event) => setContentType(event.target.value)}
          displayEmpty
          className={classes.selectEmpty}
          inputProps={{ 'aria-label': 'Content type' }}
        >
          <MenuItem value="" disabled>
            Content type
          </MenuItem>
          <MenuItem value="text/plain">Plain</MenuItem>
          <MenuItem value="text/markdown">Markdown</MenuItem>
          <MenuItem value="application/base64">Base64</MenuItem>
          <MenuItem value="image/png;base64">PNG</MenuItem>
          <MenuItem value="image/jpeg;base64">JPEG</MenuItem>
        </Select>
      </FormControl>
      <input type="file" accept="image/png, image/jpeg" onChange={handleFileChange} />

      <FormControl className={classes.formControl}>
        <Select
          required
          value={visibility}
          onChange={(event) => setVisibility(event.target.value)}
          displayEmpty
          className={classes.selectEmpty}
          inputProps={{ 'aria-label': 'Visibility' }}
        >
          <MenuItem value="" disabled>
            Visibility
          </MenuItem>
          <MenuItem value="PUBLIC">PUBLIC</MenuItem>
          <MenuItem value="PRIVATE">PRIVATE</MenuItem>
          <MenuItem value="FRIENDS">FRIENDS</MenuItem>
        </Select>
      </FormControl>
      <TextField
        required
        fullWidth
        label="Content"
        value={content}
        onChange={(event) => setContent(event.target.value)}
      />
     
      <Button variant="contained" color="primary" type="submit" onClick={handleSubmit}>
       POST 
      </Button>
    </form>
  );
};
export default CreatePost;

