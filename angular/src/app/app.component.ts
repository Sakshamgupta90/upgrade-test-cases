import {
  Component,
  ComponentFactoryResolver,
  Injectable,
  OnInit,
  ViewChild,
  ViewContainerRef,
} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CanActivate, Router } from '@angular/router';

interface User {
  name: string;
}

@Injectable()
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(): boolean {
    const loggedIn = !!localStorage.getItem('token');
    if (!loggedIn) {
      this.router.navigate(['/login']);
    }
    return loggedIn;
  }
}

@Component({
  selector: 'app-dashboard',
  template: '<p>Dashboard</p>',
})
export class DashboardComponent {}

@Component({
  selector: 'app-root',
  template: `
    <h1>{{ title }}</h1>
    <ul *ngIf="users.length; else empty">
      <li *ngFor="let user of users">{{ user.name }}</li>
    </ul>
    <ng-template #empty><p>No users yet</p></ng-template>
    <ng-container #widgetHost></ng-container>
    <router-outlet></router-outlet>
  `,
})
export class AppComponent implements OnInit {
  title = 'Admin';
  users: User[] = [];

  @ViewChild('widgetHost', { read: ViewContainerRef, static: true })
  widgetHost!: ViewContainerRef;

  constructor(private http: HttpClient, private resolver: ComponentFactoryResolver) {}

  async ngOnInit() {
    this.users = await this.http.get<User[]>('/api/users').toPromise();
    const factory = this.resolver.resolveComponentFactory(DashboardComponent);
    this.widgetHost.createComponent(factory);
  }
}
