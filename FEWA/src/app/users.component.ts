import { Component } from '@angular/core';
import { RouterOutlet, RouterModule } from '@angular/router';
import { DataService } from './data.service';
import { CommonModule } from '@angular/common';
import { WebService } from './web.service'; 
import { FormsModule } from '@angular/forms'; 
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'users',
  standalone: true,
  imports: [RouterOutlet, CommonModule, RouterModule, FormsModule],
  providers: [DataService, WebService],
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css'] // Note the plural: 'styleUrls'
})
export class UsersComponent {
    // Properties for managing users and their state.
    page: number = 1; // Current page for pagination.
    user_list: any[] = []; // List of users to be displayed.
    totalPages: number = 0; // Total number of pages.
    usersExistOnNextPage: boolean = true; // Flag to check if more users exist on the next page.

    isAuthenticated: boolean = false; // Tracks if the user is authenticated.
    isAdmin: boolean = false; // Tracks if the user has admin privileges.
    adminEmails: string[] = ['joem@glen.net', 'mckenna-j28@ulster.ac.uk', 'roryk@glen.net', 'adams@glen.net', 'davidd@glen.net', 'johnm@glen.net', 'stephenc@glen.net']; // List of admin emails.


    newUser = { name: '', username: '', password: '', email: '', admin: false }; // Object for binding to the add user form.
    showAddUserForm = false; // Toggles visibility of the add-user form.

    constructor(public dataService: DataService, public webService: WebService, public authService: AuthService) {}

    // Initialize the component.
    ngOnInit() {
        // Restore the last visited page number from session storage if available.
        if (sessionStorage['userPage']) {
            this.page = Number(sessionStorage['userPage']);
        }

        // Check authentication and fetch users.
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

        // Fetch total pages and initial user data.
        this.updateLastPageNumber();
        this.fetchUsers();
    }

    // Update the total number of pages from the backend.
    updateLastPageNumber(): void {
        this.webService.getLastPageNumberForUsers().subscribe({
            next: (lastPageNumber) => { this.totalPages = lastPageNumber; },
            error: (error) => { console.error('Failed to fetch total pages:', error); }
        });
    }

    // Navigate to the previous page.
    previousPage() {
        if (this.page > 1) {
            this.page--;
            sessionStorage['userPage'] = this.page; // Save page to session storage
            this.fetchUsers();
        }
    }

    // Navigate to the next page.
    nextPage(): void {
        if (this.page < this.totalPages) {
            this.page++;
            sessionStorage['userPage'] = this.page; // Save page to session storage
            this.fetchUsers();
        }
    }

    // Ensure efficient rendering by providing unique identifiers for users.
    trackByFn(index: number, item: any): any {
        return item._id || index; // Return `_id` if available, otherwise fallback to the index.
    }

    // Fetch the list of users for the current page.
    fetchUsers(): void {
        this.webService.getUsers(this.page).subscribe({
            next: (response) => { 
                this.user_list = response; 
            },
            error: (error) => { 
                console.error('Failed to fetch users:', error); }
        });
    }

    // Add a new user via the form.
    addUser(): void {
        console.log('Form submitted:', this.newUser); // Log the form submission for debugging.
        this.webService.addUser(this.newUser).subscribe({
            next: (response) => {
                console.log('User added successfully:', response);
                this.fetchUsers(); // Refresh the user list.
                this.showAddUserForm = false; // Hide the add-user form.
                // Reset the form with default values.
                this.newUser = { name: '', username: '', password: '', email: '', admin: false }; 
            },
            error: (error) => {
                console.error('Failed to add user:', error);
            }
        });
    }
    
}
