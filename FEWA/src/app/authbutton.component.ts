import { Component, Inject } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { DOCUMENT } from '@angular/common';
import { AsyncPipe } from '@angular/common';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';


@Component({
    selector: 'auth-button',
    templateUrl: 'authbutton.component.html',
    standalone: true,
    imports: [AsyncPipe, CommonModule],
    providers: [Router],
    styleUrls: ['./authbutton.component.css']
})


export class AuthButtonComponent {

    constructor(@Inject(DOCUMENT) public document: Document,
                public auth: AuthService,
                public router: Router) {}

}