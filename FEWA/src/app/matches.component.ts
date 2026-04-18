import { Component } from '@angular/core';
import { RouterOutlet, RouterModule, Router } from '@angular/router';
import { DataService } from './data.service';
import { WebService } from './web.service';
import { FormsModule } from '@angular/forms'; 
import { CommonModule } from '@angular/common';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'matches',
  standalone: true,
  imports: [RouterOutlet, RouterModule, FormsModule, CommonModule],
  providers: [DataService, WebService],
  templateUrl: './matches.component.html',
  styleUrl: './matches.component.css'
})
export class MatchesComponent {
    // Properties to manage matches and user authentication states.
    match_list: any[] = []; // List of matches to display.
    page: number = 1; // Current page number for pagination.
    totalPages: number = 0; // Total number of pages.
    matchesExistOnNextPage: boolean = true; // Flag to check if matches exist on the next page.
    isAuthenticated: boolean = false; // Authentication state of the user.
    isAdmin: boolean = false; // Admin status of the user.
    adminEmails: string[] = ['joem@glen.net', 'mckenna-j28@ulster.ac.uk', 'roryk@glen.net', 'adams@glen.net', 'davidd@glen.net', 'johnm@glen.net', 'stephenc@glen.net']; // List of admin emails.

    newMatch = { HomeTeam: '', AwayTeam: '', Date: '', VideoURL: '' }; // Default form values for a new match.
    showAddMatchForm = false; // Flag to toggle the visibility of the match form.

    constructor(public dataService: DataService,
                public webService: WebService,
                public authService: AuthService
    ) {}

    // Initialize the component.
    ngOnInit() {
      // Restore the page number from session storage if available.
        if (sessionStorage['page']) {
            this.page = Number(sessionStorage['page']);
        }

        // Fetch total pages and initial matches.
        this.updateLastPageNumber();
        this.fetchMatches();

        // Check user authentication and determine if they are an admin.
        this.authService.isAuthenticated$.subscribe({
          next: (isAuthenticated) => {
            this.isAuthenticated = isAuthenticated;
      
            // Check if user is an admin
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

    // Update the total number of pages from the backend.
    updateLastPageNumber(): void {
        this.webService.getLastPageNumberForMatches().subscribe({
          next: (lastPageNumber) => {
            this.totalPages = lastPageNumber; // Update total pages dynamically
          },
          error: (error) => {
            console.error('Failed to fetch last page number from backend:', error);
          },
        });
    }

    // Navigate to the previous page if it exists.
    previousPage() {
        if (this.page > 1) {
            this.page = this.page - 1;
            sessionStorage['page'] = this.page;
            //this.webService.getMatches(this.page)
            //.subscribe((response) => { this.match_list = response;
            //})
            this.fetchMatches();
        }
    }

    // Navigate to the next page if it exists.
    nextPage(): void {
        this.webService.getLastPageNumberForMatches().subscribe({
          next: (lastPageNumber) => {
            if (this.page < lastPageNumber) {
              this.page++; // Increment the page number
              sessionStorage['page'] = this.page; // Store the current page number
              this.fetchMatches(); // Fetch matches for the new page
            } else {
              console.log('Already at the last page.'); // Debugging output
            }
          },
          error: (error) => {
            console.error('Failed to fetch last page number:', error);
          }
        });
      }
      
    // Track items in a list for better performance.
    trackByMatchId(index: number, match: any): string {
        return match._id || index; // Use `_id` if available; fallback to the index
      }
      
    // Fetch matches for the current page.
    fetchMatches(): void {
        this.webService.getMatches(this.page).subscribe({
          next: (response) => {
            this.match_list = response;
          },
          error: (error) => {
            console.error('Failed to fetch matches:', error);
          }
        });
      }

    // Add a new match using form data.
    addMatch(): void {
        console.log('Form submitted:', this.newMatch);
        this.webService.addMatch(this.newMatch).subscribe({
          next: (response) => {
            console.log('Match added:', response);
            this.fetchMatches();
            this.showAddMatchForm = false;
            this.newMatch = { HomeTeam: '', AwayTeam: '', Date: '', VideoURL: '' };
          },
          error: (error) => {
            console.error('Failed to add match:', error);
          }
        });
    }
 }