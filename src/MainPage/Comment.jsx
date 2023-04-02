import * as React from 'react';

import { Avatar, Typography, ListItem, ListItemAvatar, ListItemText} from '@material-ui/core';
import { AccountCircle } from '@material-ui/icons';

function CommentItem({
    author,
    comment,
    contentType,
    published
}) {

    return (
        <ListItem alignItems="flex-start">
            <ListItemAvatar>
                {/* <Avatar variant="rounded" src={author.profileImage}/> */}
                <AccountCircle fontSize='large'></AccountCircle>
            </ListItemAvatar>
            <ListItemText
                primary={comment}
                secondary={
                <React.Fragment>
                    <Typography style={{ color: '#a3a3a3' }}>
                        {author.displayName + " — " + published.substring(0,10)}
                    </Typography>
                </React.Fragment>
                }
            />
        </ListItem>
    );
}
export default CommentItem;