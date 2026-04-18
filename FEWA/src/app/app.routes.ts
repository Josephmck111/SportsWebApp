import { Routes } from '@angular/router';
import { HomeComponent } from './home.component';
import { MatchesComponent } from './matches.component';
import { TeamsComponent } from './teams.component';
import { UsersComponent } from './users.component';
import { MatchComponent } from './match.component';
import { TeamComponent } from './team.component';
import { UserComponent } from './user.component';


  


export const routes: Routes = [
    {
        path: '',
        component: HomeComponent
    },
    {
        path: 'matches',
        component: MatchesComponent
    },
    {
        path: 'matches/:id',
        component: MatchComponent
    },
    {
        path: 'teams',
        component: TeamsComponent
    },
    {
        path: 'teams/:id',
        component: TeamComponent
    },
    {
        path: 'users',
        component: UsersComponent
    },
    {
        path: 'users/:id',
        component: UserComponent
    }
];
