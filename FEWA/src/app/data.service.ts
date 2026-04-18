import matchesData from '../assets/matches.json';
import teamsData from '../assets/teams.json'
import usersData from '../assets/users.json'; 


export class DataService {
    pageSize: number = 5;

    // Matches functionality
    getMatches(page: number) {
        let pageStart = (page - 1) * this.pageSize;
        let pageEnd = pageStart + this.pageSize;
        return matchesData.slice(pageStart, pageEnd);
    }

    getLastPageNumberForMatches() {
        return Math.ceil(matchesData.length / this.pageSize);
    }

    // Teams functionality
    getTeams(page: number) {
        let pageStart = (page - 1) * this.pageSize;
        let pageEnd = pageStart + this.pageSize;
        return teamsData.slice(pageStart, pageEnd);
    }

    getLastPageNumberForTeams() {
        return Math.ceil(teamsData.length / this.pageSize);
    }

    // Users functionality
    getUsers(page: number) {
        let pageStart = (page - 1) * this.pageSize;
        let pageEnd = pageStart + this.pageSize;
        return usersData.slice(pageStart, pageEnd);
    }

    getLastPageNumberForUsers() {
        return Math.ceil(usersData.length / this.pageSize);
    }

    getMatch(id: any) {
        let dataToReturn: any[] = [];
        matchesData.forEach( function(match) {
            if (match['_id']['$oid'] == id) {
                dataToReturn.push( match );
            }
        })
        return dataToReturn;
    }

    //getTeam(id: any) {
        //let dataToReturn: any[] = [];
        //teamsData.forEach( function(team) {
           // if (team['_id']['$oid'] == id) {
             //   dataToReturn.push( team );
            //}
      //  })
    //    return dataToReturn;
   // }

    getUser(id: any) {
        let dataToReturn: any[] = [];
        usersData.forEach( function(user) {
            if (user['_id']['$oid'] == id) {
                dataToReturn.push( user );
            }
        })
        return dataToReturn;
    }
    populateComments() {
        matchesData.forEach(match => {
          if (!match.Comments) {
            match.Comments = []; 
          }
          if (match.Comments.length === 0) {
            const defaultComment = {
              username: 'User 1',
              text: 'This is a sample review for testing.',
            };
            match.Comments.push(defaultComment);
          }
        });
    }

    postComment(id: any, comment: any) {
        matchesData.forEach(match => {
            if (!match.Comments) {
                match.Comments = [];
            }
            if (match['_id']['$oid'] === id) {
                const newComment = {
                    username: comment.username,
                    text: comment.text,
                };

                match.Comments.push(newComment);
            }
        });
    }     
}
