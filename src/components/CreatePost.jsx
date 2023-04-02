import * as React from 'react';
import { useState } from 'react';
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
  const [contentType, setContentType] = useState('');
  const [content, setContent] = useState('');
  const [visibility, setVisibility] = useState('');
  const [unlisted, setUnlisted] = useState(false);
  const [categories, setCategories] = useState([]);
  const author = JSON.parse(window.localStorage.getItem("Author"));
  const AUTHOR_ID = author.id;

  
  const handleSubmit = async (event) => {
    event.preventDefault();
  
    const postData = {
      title: title,
      description: description,
      contentType: contentType,
      content: content,
      visibility: visibility,
      unlisted: unlisted,
      categories: categories,
    };
  
    if (visibility === "PUBLIC") {
      try {
        const response = await axios.post(AUTHOR_ID+'posts/', JSON.stringify(postData));
        console.log(response.data);
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

        for (const friend of friends) {
          try {
            console.log('friend:',friend);
            const response = await axios.post(friend+'inbox/', JSON.stringify(postData),{
              headers:{'Content-Type': 'text/plain'}
          });
            console.log('friend post:',response.data);
          } catch (error) {
            console.error(error);
          }
        }
  
        const publicResponse = await axios.post(AUTHOR_ID+'posts/', postData);
        console.log('mypost:',publicResponse.data);
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
        const response = await axios.post(private_author.id+'inbox/', postData,{
          headers:{'Content-Type': 'text/plain'}
        });
        console.log('private post:',response.data);
  
        const publicResponse = await axios.post(AUTHOR_ID+'posts/', postData);
        console.log(publicResponse.data);
      } catch (error) {
        console.error(error);
      }
    }
  };
    
  //   fetch('/service/authors/'+ AUTHOR_ID+ '/posts/', {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json'
  //     },
  //     body: JSON.stringify(postData)
  //   })
  //     .then(response => response.json())
  //     .then(data => console.log(data))
  //     //.catch(error => console.error(error));
  // };

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
          value={contentType}
          onChange={(event) => setContentType(event.target.value)}
          displayEmpty
          className={classes.selectEmpty}
          inputProps={{ 'aria-label': 'Content type' }}
        >
          <MenuItem value="" disabled>
            Content type
          </MenuItem>
          <MenuItem value="Plain">Plain</MenuItem>
          <MenuItem value="Markdown">Markdown</MenuItem>
          <MenuItem value="Base64">Base64</MenuItem>
          <MenuItem value="PNG">PNG</MenuItem>
          <MenuItem value="JPEG">JPEG</MenuItem>
        </Select>
      </FormControl>

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
      {/* <FormControlLabel className={classes.checkbox}
        control={
          <Checkbox
            checked={unlisted}
            onChange={(event) => setUnlisted(event.target.checked)}
            name="unlisted"
          />
        }
        label="Unlisted"
      /> */}
      <TextField
        required
        fullWidth
        label="Content"
        value={content}
        onChange={(event) => setContent(event.target.value)}
      />
     
      <Button variant="contained" color="primary" type="submit">
        POST
      </Button>
    </form>
  );
};
export default CreatePost;

