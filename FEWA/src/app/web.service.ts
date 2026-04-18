import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { map } from 'rxjs/operators';


@Injectable()
export class WebService{

    pageSize: number = 10;

    constructor(private http: HttpClient) { }

    getMatches(page: number) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/matches?pn=' +
            page + '&ps=' + this.pageSize);
    }

    getMatch(id: any) {
        return this.http.get<any>(
        'http://localhost:5000/api/v1.0/matches/' + id);
    }

    getLastPageNumberForMatches(): Observable<number> {
        return this.http.get<{ total_count: number }>('http://localhost:5000/api/v1.0/matches/count').pipe(
          map((response) => Math.ceil(response.total_count / this.pageSize))
        );
      }
    

    getComments(id: any) {
        return this.http.get<any>('http://localhost:5000/api/v1.0/matches/' + id + '/comments');
    }

    postComment(id: any, comment: any) {
        let postData = new FormData();
        postData.append("username", comment.username);
        postData.append("text", comment.text);
        return this.http.post<any>(
            'http://localhost:5000/api/v1.0/matches/' +
            id + "/comments", postData);
    }

    getTeams(page: number) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/teams?pn=' +
            page + '&ps=' + this.pageSize);
    }

    getLastPageNumberForTeams(): Observable<number> {
        return this.http.get<{ total_count: number }>('http://localhost:5000/api/v1.0/teams/count').pipe(
            map((response) => Math.ceil(response.total_count / this.pageSize))
          );
    }

    getUsers(page: number) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/users?pn=' +
            page + '&ps=' + this.pageSize);
    }

    getTeam(id: any) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/teams/' + id);
    }

    getUser(id: any) {
        return this.http.get<any>(
            'http://localhost:5000/api/v1.0/users/' + id);
    }

    uploadVideo(id: string, formData: FormData): Observable<any> {
        return this.http.post<any>(
          `http://localhost:5000/api/v1.0/matches/${id}/uploads`,
          formData
        );
    }
      
    getVideo(id: string): Observable<any> {
        return this.http.get<any>(`http://localhost:5000/api/v1.0/matches/${id}/uploads`);
    }

    deleteVideo(id: string): Observable<any> {
        return this.http.delete<any>(`http://localhost:5000/api/v1.0/matches/${id}/uploads`);
    }
    
    addMatch(match: any): Observable<any> {
        const formData = new FormData();
        formData.append('HomeTeam', match.HomeTeam);
        formData.append('AwayTeam', match.AwayTeam);
        formData.append('Date', match.Date);
        formData.append('VideoURL', match.VideoURL || '');
        return this.http.post<any>('http://localhost:5000/api/v1.0/matches', formData);
    }

    addTeam(team: any): Observable<any> {
        const formData = new FormData();
        formData.append('Team', team.Team);
        formData.append('Division', team.Division);
        formData.append('Players', team.Players);
        return this.http.post<any>('http://localhost:5000/api/v1.0/teams', formData);
    }

    addUser(user: any): Observable<any> {
        const formData = new FormData();
        formData.append('name', user.name);
        formData.append('username', user.username);
        formData.append('password', user.password); // Submit plain text (converted to binary in backend)
        formData.append('email', user.email);
        formData.append('admin', String(user.admin)); // Convert boolean to string
        return this.http.post<any>('http://localhost:5000/api/v1.0/users', formData);
    }

    getLastPageNumberForUsers(): Observable<number> {
        return this.http.get<{ total_count: number }>('http://localhost:5000/api/v1.0/users/count').pipe(
            map(response => Math.ceil(response.total_count / this.pageSize))
        );
    }

    updateUser(user: any): Observable<any> {
        const formData = new FormData();
        formData.append('name', user.name);
        formData.append('username', user.username);
        formData.append('password', user.password); // Ensure password is handled properly
        formData.append('email', user.email);
        formData.append('admin', String(user.admin));
        return this.http.put<any>(`http://localhost:5000/api/v1.0/users/${user._id}`, formData);
    }

    updateTeam(team: any): Observable<any> {
        const formData = new FormData();
        formData.append('Team', team.Team);
        formData.append('Division', team.Division);
        formData.append('Players', team.Players);
        return this.http.put<any>(`http://localhost:5000/api/v1.0/teams/${team._id}`, formData);
    }

    updateMatch(match: any): Observable<any> {
        const formData = new FormData();
        formData.append('HomeTeam', match.HomeTeam);
        formData.append('AwayTeam', match.AwayTeam);
        formData.append('Date', match.Date);
        return this.http.put<any>(`http://localhost:5000/api/v1.0/matches/${match._id}`, formData);
    }

    deleteUser(id: string): Observable<any> {
        return this.http.delete<any>(`http://localhost:5000/api/v1.0/users/${id}`);
    }

    deleteTeam(id: string): Observable<any> {
        return this.http.delete<any>(`http://localhost:5000/api/v1.0/teams/${id}`);
    }

    deleteMatch(id: string): Observable<any> {
        return this.http.delete<any>(`http://localhost:5000/api/v1.0/matches/${id}`);
    }

    deleteComment(matchId: string, commentId: string): Observable<any> {
        return this.http.delete<any>(`http://localhost:5000/api/v1.0/matches/${matchId}/comments/${commentId}`);
    }
    

    
    
}