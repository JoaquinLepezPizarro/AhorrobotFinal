import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { Observable } from 'rxjs';
import {Productos} from '../interfaces/productos';

@Injectable({
  providedIn: 'root'
})

export class AppService {

  servidor = "http://127.0.0.1:3000";

  productos: Productos[] = []

  constructor(private servicio:HttpClient) { }

  mostrarProductosMasBaratos(nombreProducto:any):Observable<any> {
    //console.log(`ESTOY EN EL SERVICE: ${nombreProducto}`);
    return this.servicio.get(`${this.servidor}/productos_vigentes/:${nombreProducto}`);
  }

  mostrarFarmacias():Observable<any> {
    //console.log(`ESTOY EN EL SERVICE: ${idFarmacia}`);
    return this.servicio.get(`${this.servidor}/farmacias`);
  }
}
