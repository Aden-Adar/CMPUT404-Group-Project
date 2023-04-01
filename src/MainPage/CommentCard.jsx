import * as React from 'react';

import { Avatar, Card, CardHeader, Typography, Link} from '@material-ui/core';
import { AccountCircle } from '@material-ui/icons';

function CommentCard({
    author,
    comment,
    published
}) {

    return (
        <Card variant='outlined'>
          <CardHeader
            avatar={<AccountCircle fontSize='large'></AccountCircle>}
            title={
              <span>
                <Typography component="span" variant="body1">{author.displayName + " commented: " + comment + " on your post! (" + published.substring(0,10) + ")"}</Typography>
              </span>}
          />
        </Card>
    );
}
export default CommentCard;