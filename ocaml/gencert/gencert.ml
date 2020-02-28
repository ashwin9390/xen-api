(*
 * Copyright (C) Citrix Systems Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published
 * by the Free Software Foundation; version 2.1 only. with the special
 * exception on linking described in file LICENSE.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Lesser General Public License for more details.
 *)

(* Usage: gencert <path> *)

let inventory = "/etc/xensource-inventory"
let generate_ssl_cert = "/opt/xensource/libexec/generate_ssl_cert"

module Lib = Gencertlib.Lib

let generate_cert_or_fail ~path ~cn =
  let args = [path; cn] in
  let (stdout, stderr) = Forkhelpers.execute_command_get_output generate_ssl_cert args in

  Printf.printf {|generate_ssl_cert stdout: "%s"|} stdout;
  Printf.printf {|generate_ssl_cert stderr: "%s"|} stderr;
  if Sys.file_exists path then
    Printf.printf "file exists (%s), assuming cert was created" path
  else begin
    Printf.eprintf "file doesn't exist (%s): cert was not created" path;
    exit 1
  end

let main ~dbg ~path =
  let init_inventory () =
    Inventory.inventory_filename := inventory
  in
  init_inventory ();
  let hostname = Unix.gethostname () in
  let cn =
    if Astring.String.is_prefix ~affix:"localhost" hostname then
      Lib.get_management_ip_addr ~dbg
    else if Astring.String.is_infix ~affix:"." hostname then
      None
    else
      Lib.get_management_ip_addr ~dbg
  in
  let cn = Option.value ~default:hostname cn in
  generate_cert_or_fail ~path ~cn

let () =
  let dbg = Printf.sprintf "gencert - %f" (Unix.gettimeofday ()) in

  if Array.length Sys.argv <> 2 then begin
    Printf.eprintf "Usage: gencert PATH";
    exit 1
  end;

  let path = Sys.argv.(1) in

  if Sys.file_exists path then begin
      Printf.printf "file already exists at path (%s) - doing nothing" path;
      exit 0
    end
  else
    main ~dbg ~path
