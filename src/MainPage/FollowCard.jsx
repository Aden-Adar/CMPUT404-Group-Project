import * as React from 'react';

import { Avatar, Card, CardHeader, Typography, Link, IconButton} from '@material-ui/core';
import { AccountCircle, Check, Close } from '@material-ui/icons';

function FollowCard({
    summary,
    actor,
    object
}) {
    function handleAccept() {
        async function putRequest() {
            let splitID = actor.id.split('/')
            let foreignID = splitID[splitID.length - 2]
            let response = await fetch(object.id +'followers/' + foreignID + '/', {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              }
            })
            let res_data = await response.json()
        }
        putRequest()
    }

    function handleDecline() {
        
    }

    return (
        <Card variant='outlined'>
          <CardHeader
            avatar={<AccountCircle fontSize='large'></AccountCircle>}
            title={
              <span>
                <Typography component="span" variant="body1">{summary + "(you)!"}</Typography>
              </span>}
          />
          <IconButton aria-label="accept" onClick={handleAccept}>
              <Check style={{ color: 'green'}}/>
            </IconButton>
            <IconButton aria-label="decline" onClick={handleDecline}>
              <Close style={{ color: 'red' }}/>
            </IconButton>
        </Card>
    );
}
export default FollowCard;