import * as React from 'react';

import { Avatar, Card, CardHeader, Typography, Link} from '@material-ui/core';
import { AccountCircle } from '@material-ui/icons';

function LikeCard({
    author,
    summary,
    object
}) {

    return (
        <Card variant='outlined'>
          <CardHeader
            avatar={<AccountCircle fontSize='large'></AccountCircle>}
            title={
              <span>
                <Typography component="span" variant="body1" href={object}>{summary + "!" }</Typography>
              </span>}
          />
        </Card>
    );
}
export default LikeCard;