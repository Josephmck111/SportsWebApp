import { Component } from '@angular/core';
import { RouterOutlet, RouterModule, Router } from '@angular/router';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';
import { WebService } from './web.service'; 
import { FormsModule } from '@angular/forms'; 
import { AuthService } from '@auth0/auth0-angular';

@Component({
    selector: 'teams',
    standalone: true,
    imports: [RouterOutlet, CommonModule, RouterModule, FormsModule], 
    providers: [DataService, WebService],
    templateUrl: './teams.component.html',
    styleUrl: './teams.component.css'
})
export class TeamsComponent {
    // Properties for managing teams and user information.
    team_list: any; // List of teams to display.
    totalPages: number = 0; // Total number of pages for pagination.
    page: number = 1; // Current page number.
    teamsExistOnNextPage: boolean = true; // Tracks whether there are more teams on the next page.
    isAuthenticated: boolean = false; // Indicates whether the user is authenticated.
    isAdmin: boolean = false; // Indicates whether the user is an admin.
    adminEmails: string[] = ['joem@glen.net', 'mckenna-j28@ulster.ac.uk', 'roryk@glen.net', 'adams@glen.net', 'davidd@glen.net', 'johnm@glen.net', 'stephenc@glen.net']; // List of admin emails.

    newTeam = { Team: '', Division: '', Players: ''}; // Default values for the new team form.
    showAddTeamForm = false; // Toggles visibility of the add-team form.


    constructor(public dataService: DataService,
                public webService: WebService,
                public authService: AuthService
    ) {}

    // Initialize the component.
    ngOnInit() {
        // Restore the last visited page from session storage if available.
        if (sessionStorage['teamPage']) {
            this.page = Number(sessionStorage['teamPage']);
        }

        // Fetch the total number of pages and the initial list of teams.
        this.updateLastPageNumber();
        this.fetchTeams();

        // Subscribe to authentication changes and determine admin privileges if authenticated.
        this.authService.isAuthenticated$.subscribe({
          next: (isAuthenticated) => {
            this.isAuthenticated = isAuthenticated;
      
            // If authenticated, check if the user is an admin based on their email.
            if (isAuthenticated) {
              this.authService.user$.subscribe({
                next: (user) => {
                  this.isAdmin = this.adminEmails.includes(user?.email || '');
                },
                error: (error) => {
                  console.error('Failed to retrieve user details:', error);
                },
              });
            }
          },
          error: (error) => {
            console.error('Failed to determine authentication status:', error);
          },
        });
    }

    // Fetch and update the total number of pages from the backend.
    updateLastPageNumber(): void {
        this.webService.getLastPageNumberForTeams().subscribe({
          next: (lastPageNumber) => {
            this.totalPages = lastPageNumber; // Update total pages dynamically
          },
          error: (error) => {
            console.error('Failed to fetch last page number from backend:', error);
          },
        });
    }

    // Navigate to the previous page of teams.
    previousPage() {
        if (this.page > 1) {
            this.page = this.page - 1;
            sessionStorage['teamPage'] = this.page;
            //this.webService.getTeams(this.page)
            //.subscribe((response) => { this.team_list = response;
            //})
            this.fetchTeams();
        }
    }

    // Navigate to the next page of teams.
    nextPage(): void {
        this.webService.getLastPageNumberForTeams().subscribe({
          next: (lastPageNumber) => {
            if (this.page < lastPageNumber) {
              this.page++; // Increment the page number
              sessionStorage['page'] = this.page; // Store the current page number
              this.fetchTeams(); // Fetch matches for the new page
            } else {
              console.log('Already at the last page.'); // Debugging output
            }
          },
          error: (error) => {
            console.error('Failed to fetch last page number:', error);
          }
        });
    }

    // Track individual teams in the list by their unique ID for better performance.
    trackByTeamId(index: number, team: any): string {
        return team._id || index; // Use `_id` if available; fallback to the index
    }
      
    // Fetch the list of teams for the current page.
    fetchTeams(): void {
        this.webService.getTeams(this.page).subscribe({
          next: (response) => {
            this.team_list = response;
          },
          error: (error) => {
            console.error('Failed to fetch teams:', error);
          }
        });
    }

    // Add a new team using the form data.
    addTeam(): void {
        console.log('Form submitted:', this.newTeam);
        this.webService.addTeam(this.newTeam).subscribe({
          next: (response) => {
            console.log('Team added:', response);
            this.fetchTeams();
            this.showAddTeamForm = false;
            this.newTeam = { Team: '', Division: '', Players: ''};
          },
          error: (error) => {
            console.error('Failed to add team:', error);
          }
        });
    }      
}
