import { Component } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { AsyncPipe } from '@angular/common';
import { CommonModule } from '@angular/common';
import { map } from 'rxjs/operators';

@Component({
    selector: 'user-profile',
    templateUrl: 'authuser.component.html',
    standalone: true,
    imports: [AsyncPipe, CommonModule]
})
export class AuthUserComponent {
    isAdmin: boolean = false; 

    constructor(public auth: AuthService) {
        this.auth.user$
            .pipe(map((user: any) => user?.['role'] === 'admin')) 
            .subscribe((isAdmin) => {
                this.isAdmin = isAdmin;
            });
    }
}
